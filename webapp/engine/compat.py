"""Python 3.12 compatibility for the engine.

Up to Python 3.11, random.randint()/randrange() accepted floats with an
integral value (e.g. the result of round(x, 0)); 3.12 raises TypeError.  The
engine relies on the old behaviour in Penalty, YardageTable and Play, so wrap
the two functions to coerce integral floats.  Non-integral floats still raise,
exactly as before.  Import this module before any engine module.
"""
import random as _random

_orig_randint = _random.randint
_orig_randrange = _random.randrange


def _int_if_integral(x):
    if isinstance(x, float) and x.is_integer():
        return int(x)
    return x


def randint(a, b):
    return _orig_randint(_int_if_integral(a), _int_if_integral(b))


def randrange(start, stop=None, step=1):
    if stop is None:
        return _orig_randrange(_int_if_integral(start))
    return _orig_randrange(_int_if_integral(start), _int_if_integral(stop), _int_if_integral(step))


if not getattr(_random, "_gridiron_compat", False):
    _random.randint = randint
    _random.randrange = randrange
    _random._gridiron_compat = True
