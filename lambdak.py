# lambdak.py - functional programming with continuations in Python

class lambdak(object):
  '''A lambda with a continuation, to allow extended calculations.'''
  def __init__(self, k, x = ()):
    self.k = k
    self.x = x if x == () else (x,)

  def __call__(self, *args, **kwargs):
    k, x = self.k, self.x

    while k is not None:
      if args != () and kwargs != {}:
        l = k(*args, **kwargs)
        args = ()
        kwargs = {}
      elif args != ():
        l = k(*args)
        args = ()
      # If x is empty tuple, *x will be expanded into no arguments.
      else: l = k(*x)

      # If we didn't get back a lambdak, then we've reached the end of
      # the lambdak chain, and it's time to stop.
      if not isinstance(l, lambdak): return l
      k, x = l.k, l.x

    # If the lambdak we got back didn't have a continuation function,
    # then it's also time to stop.
    return None if x == () else x[0]

def call_(k, *args): return None if k is None else k(*args)

def return_(x): return x

def given_(k): return lambdak(k)

def do_(expr_k, k = None):
  def act():
    expr_k()
    return call_(k)

  return lambdak(act)

def print_(x, k = None):
  def act():
    print x
    return call_(k)

  return lambdak(act)

def assert_(expr, k = None):
  def act():
    assert expr
    return call_(k)

  return lambdak(act)

def raise_(ex_type = None, ex_val = None, tb_val = None):
  def act():
    if ex_type is None: raise
    else: raise ex_type, ex_val, tb_val

  return lambdak(act)

def cond_(test_pairs, default_expr, k = None):
  for (test_expr, then_expr) in test_pairs:
    if test_expr(): return lambdak(k, then_expr())
  else: return lambdak(k, call_(default_expr))

def import_(mod_name, k):
  def act():
    m = __import__(mod_name)
    return call_(k, m)

  return lambdak(act)

def try_(expr_k, except_k, finally_k = None):
  def act():
    try: lambdak(expr_k)()
    except: lambdak(except_k)()
    finally: return call_(finally_k)

  return lambdak(act)

def for_(seq, act_k, k = None):
  def act():
    for x in seq: lambdak(act_k, x)()
    return call_(k)

  return lambdak(act)

def setattr_(x, attr_name, attr_val, k = None):
  return do_(lambda: setattr(x, attr_name, attr_val), k)

def delattr_(x, attr_name, k = None):
  return do_(lambda: delattr(x, attr_name), k)

def with_(expr_k, act_k, k = None):
  def act():
    with expr_k() as x:
      if x is None: lambdak(act_k)()
      else: lambdak(act_k, x)()
    return call_(k)

  return lambdak(act)

def assign_(nm, v, d, k = None):
  def act():
    d[nm] = v
    return call_(k)

  return lambdak(act)

def get_(nm, d): return d[nm]

def del_(nm, d, k = None):
  def act():
    del d[nm]
    return call_(k)

  return lambdak(act)

