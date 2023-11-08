import weakref
from functools import lru_cache, wraps


def weak_lru(maxsize=128, typed=False):
  'LRU Cache decorator that keeps a weak reference to "self"'

  def wrapper(func):

    @lru_cache(maxsize, typed)
    def _func(_self, *args, **kwargs):
      return func(_self(), *args, **kwargs)

    @wraps(func)
    def inner(self, *args, **kwargs):
      return _func(weakref.ref(self), *args, **kwargs)

    return inner

  return wrapper


def complement_argnums(argnums, num_args):
  argnums = (argnums,) if isinstance(argnums, int) else argnums
  complement = []
  a = 0
  for i in range(num_args):
    if a < len(argnums) and i == argnums[a]:
      a += 1
    else:
      complement.append(i)
  return tuple(complement)
