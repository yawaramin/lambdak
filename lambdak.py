# lambdak.py - functional programming with continuations in Python

class lambdak(object):
  '''A lambda with a continuation, to allow extended calculations.'''
  def __init__(self, k, x = None):
    (self.k, self.x) = (k, x)

  def __call__(self):
    (k, x) = (self.k, self.x)

    while k is not None:
      l = k() if x is None else k(x)
      if l is None: return
      (k, x) = (l.k, l.x)

def __call_k(k): return None if k is None else k()

def print_(x, k = None):
  def act():
    print x
    return __call_k(k)

  return lambdak(act)

def let_(expr, k = None): return lambdak(k, expr)

def assert_(expr, k = None):
  def act():
    assert expr
    return __call_k(k)

  return lambdak(act)

def if_(test_expr, then_expr, else_expr, k = None):
  if test_expr: return lambdak(k, then_expr())
  else: return lambdak(k, else_expr())

def cond_(test_pairs, default_expr, k = None):
  for (test_expr, then_expr) in test_pairs:
    if test_expr(): return lambdak(k, then_expr())
  else: return lambdak(k, default_expr())

def import_(mod_name, k = None):
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

if __name__ == "__main__":
  dispatch_dict = {
    "foo":
      print_("I pity the foo!", lambda:
      for_(range(5), lambda x:
        print_(x))),

    "bar":
      import_("math", lambda m:
      let_(5, lambda r:

      print_("The radius of the circle is:", lambda:
      print_(m.pi * r * r)))),

    "baz":
      print_("None of your bazness!") }

  dispatch_dict["bar"]()
