import time
from collections.abc import Callable
from functools import partial, wraps

from .tcr_color import color as c


def test(func: Callable) -> Callable:
  """A decorator for adding."""
  @wraps(func)
  def wrapper(*args, **kwargs):
    name = func.__name__
    print(f"""
{c('White')}####{len(name)*"#"}####
{""}### {c('Gold')}{    name     }{c('White')} ###
{""}####{len(name)*"#"}####{c('reset')}
"""[1:-1])
    return func(*args, **kwargs)

  return wrapper

def timeit(func=None, *, printhook=None, color=True, pattern="%(c_White)s%(name)s%(c_Gold)s took %(c_White)s%(time)s%(c_Gold)s seconds to execute.%(c_reset)s"):
  if func is None: return partial(timeit, printhook=printhook, pattern=pattern, color=color)
  if printhook is None: printhook = print
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    printhook(pattern % {
      'name':    func.__name__,
      'time':    f'{elapsed_time:.4f}',
      'c_White': c('White') if color else "",
      'c_Gold':  c('Gold' ) if color else "",
      'c_reset': c('reset') if color else "",
    })
    return result

  return wrapper