from __future__ import print_function, absolute_import, division

import warnings
import pkgutil
import inspect
import importlib

from sklearn.base import BaseEstimator


__all__ = ['mixtape', 'import_all_estimators']


def mixtape():
    import mixtape
    from sklearn.pipeline import Pipeline
    scope = import_all_estimators(mixtape)
    scope['Pipeline'] = Pipeline
    return scope


def import_all_estimators(pkg):

    def estimator_in_module(mod):
        for name, obj in inspect.getmembers(mod):
            if name.startswith('_'):
                continue
            if inspect.isclass(obj) and issubclass(obj, BaseEstimator):
                yield obj

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        result = {}
        for _, modname, ispkg in pkgutil.iter_modules(pkg.__path__):
            c = '%s.%s' % (pkg.__name__, modname)
            try:
                mod = importlib.import_module(c)
                if ispkg:
                    result.update(import_all_estimators(mod))
                for kls in estimator_in_module(mod):
                    result[kls.__name__] = kls
            except ImportError as e:
                print('e', e)
                continue

        return result
