from scipy import stats
import functools

class Assumption(object):
    graphs = None
    results = None

def assume_normal(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        assumes, result = func(*args, **kwargs)
        return assumes, result
    return _func
