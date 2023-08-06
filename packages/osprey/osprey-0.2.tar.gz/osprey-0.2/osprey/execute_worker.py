from __future__ import print_function, absolute_import, division

import os
import sys
import traceback
from socket import gethostname
from getpass import getuser
from datetime import datetime

from six import iteritems
from six.moves import cStringIO
from sqlalchemy import func
from sklearn.base import clone, BaseEstimator
from sklearn.grid_search import GridSearchCV

from . import __version__
from .config import Config
from .trials import Trial
from .utils import Unbuffered, format_timedelta, current_pretty_time


def execute(args, parser):
    start_time = datetime.now()
    sys.stdout = Unbuffered(sys.stdout)
    # Load the config file and extract the fields
    print_header()

    config = Config(args.config)
    estimator = config.estimator()
    session = config.trials()
    cv = config.cv()
    searchspace = config.search_space()
    engine = config.search_engine()
    seed = config.search_seed()
    config_sha1 = config.sha1()
    scoring = config.scoring()

    print('\nLoading dataset...')
    X, y = config.dataset()
    print('  %d elements with%s labels' % (len(X), 'out' if y is None else ''))
    print('Instantiated estimator:')
    print('  %r' % estimator)
    print(searchspace)

    statuses = []
    for i in range(args.n_iters):
        print('\n' + '-'*70)
        print('Beginning iteration %50s' % ('%d / %d' % (i+1, args.n_iters)))
        print('-'*70)

        # requery the history ever iteration, because another worker
        # process may have written to it in the mean time
        history = [[t.parameters, t.mean_cv_score, t.status]
                   for t in session.query(Trial).all()]
        print('History contains: %d trials' % len(history))
        print('Choosing next hyperparameters with %s...' % engine.__name__)
        params = engine(history, searchspace, seed)
        print('  %r\n' % params)
        assert len(params) == searchspace.n_dims

        s = run_single_trial(
            estimator=estimator, scoring=scoring, X=X, y=y,
            params=params, cv=cv, config_sha1=config_sha1, session=session)
        statuses.append(s)

    print_footer(statuses, start_time)


def run_single_trial(estimator, scoring, X, y, params, cv, config_sha1,
                     session):
    # make sure we get _all_ the parameters, including defaults on the
    # estimator class, to save in the database
    params = clone(estimator).set_params(**params).get_params()
    params = dict((k, v) for k, v in iteritems(params)
                  if not isinstance(v, BaseEstimator))

    t = Trial(status='PENDING', parameters=params, host=gethostname(),
              user=getuser(), started=datetime.now(),
              config_sha1=config_sha1)
    session.add(t)
    session.commit()

    try:
        grid = GridSearchCV(
            estimator, param_grid=dict((k, [v]) for k, v in iteritems(params)),
            scoring=scoring, cv=cv, verbose=1, refit=False)
        grid.fit(X, y)
        score = grid.grid_scores_[0]

        t.mean_cv_score = score.mean_validation_score
        t.cv_scores = score.cv_validation_scores.tolist()
        t.status = 'SUCCEEDED'
        best_so_far = session.query(func.max(Trial.mean_cv_score)).first()[0]
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        print('Success! Model score = %f' % t.mean_cv_score)
        print('(best score so far   = %f)' % max(t.mean_cv_score, best_so_far))
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    except (Exception, KeyboardInterrupt, SystemExit) as e:
        buf = cStringIO()
        traceback.print_exc(file=buf)

        t.traceback = buf.getvalue()
        t.status = 'FAILED'
        print('-'*78, file=sys.stderr)
        print('Exception encountered while fitting model')
        print('-'*78, file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        if isinstance(e, (KeyboardInterrupt, SystemExit)):
            sys.exit(1)
        print('-'*78, file=sys.stderr)
    finally:
        t.completed = datetime.now()
        t.elapsed = t.completed - t.started
        session.commit()

    return t.status


def print_header():
    print('='*70)
    print('= osprey is a tool for machine learning '
          'hyperparameter optimization. =')
    print('='*70)
    print()
    print('osprey version:  %s' % __version__)
    print('time:            %s' % current_pretty_time())
    print('hostname:        %s' % gethostname())
    print('cwd:             %s' % os.path.abspath(os.curdir))
    print('pid:             %s' % os.getpid())
    print()


def print_footer(statuses, start_time):
    n_successes = sum(s == 'SUCCEEDED' for s in statuses)
    elapsed = format_timedelta(datetime.now() - start_time)

    print()
    print('%d/%d models fit successfully.' % (n_successes, len(statuses)))
    print('time:         %s' % current_pretty_time())
    print('elapsed:      %s.' % elapsed)
    print('osprey worker exiting.')
