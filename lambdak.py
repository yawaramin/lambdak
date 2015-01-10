# lambdak.py - functional programming with continuations in Python

class lambdak(object):
  '''A lambda with a continuation, to allow extended calculations.'''
  def __init__(self, k, x = None):
    (self.k, self.x) = (k, x)

  def __call__(self):
    (k, x) = (self.k, self.x)

    while k is not None:
      l = k() if x is None else k(x)

      # If we didn't get back a lambdak, then we've reached the end of
      # the lambdak chain, and it's time to stop.
      if not isinstance(l, lambdak): return l
      (k, x) = (l.k, l.x)

    # If the lambdak we got back didn't have a continuation function,
    # then it's also time to stop.
    return x

def __call_k(k): return None if k is None else k()

def let_(expr, k): return lambdak(k, expr)

def do_(expr, k = None): return lambdak(k, expr)

def print_(x, k = None):
  def act():
    print x
    return __call_k(k)

  return lambdak(act)

def assert_(expr, k = None):
  def act():
    assert expr
    return __call_k(k)

  return lambdak(act)

def raise_(ex_type = None, ex_val = None, tb_val = None):
  if ex_type is None: raise
  else: raise ex_type, ex_val, tb_val

def if_(test_expr, then_expr, else_expr = None, k = None):
  if test_expr: return lambdak(k, then_expr())
  else: return lambdak(k, __call_k(else_expr))

def cond_(test_pairs, default_expr = None, k = None):
  for (test_expr, then_expr) in test_pairs:
    if test_expr(): return lambdak(k, then_expr())
  else: return lambdak(k, __call_k(default_expr))

def import_(mod_name, k):
  m = __import__(mod_name)
  return lambdak(k, m)

def try_(expr_k, except_k, finally_k = None):
  def act():
    try: lambdak(expr_k)()
    except: lambdak(except_k)()
    finally: return __call_k(finally_k)

  return lambdak(act)

def for_(seq, act_k, k = None):
  def act():
    for x in seq: lambdak(act_k, x)()
    return __call_k(k)

  return lambdak(act)

def setattr_(x, attr_name, attr_val, k = None):
  def act():
    setattr(x, attr_name, attr_val)
    return __call_k(k)

  return lambdak(act)

def delattr_(x, attr_name, k = None):
  def act():
    delattr(x, attr_name)
    return __call_k(k)

  return lambdak(act)

