from contextlib import closing, contextmanager
import StringIO as s
import unittest as t
from lambdak import *

# A helper class to test attribute access.
class A: pass

class test_lambdak(t.TestCase):
  def test_init_k_x(self):
    args = (1, 2)
    lk = lambdak(*args)

    self.assertEqual((lk.k, lk.x), (1, (2,)))

  def test_init_k(self):
    val = 1
    lk = lambdak(val)

    self.assertEqual((lk.k, lk.x), (val, ()))

class test_call_(t.TestCase):
  def test_call_none(self):
    self.assertEqual(call_(None), None)

  def test_call_func(self):
    val = 1
    def f(): return val

    self.assertEqual(call_(f), val)

class test_do_(t.TestCase):
  def setUp(self):
    self.a = A()
    self.name = "x"
    self.val = 1

  def test_do_not(self):
    "The do_ action shouldn't be carried out unless the lambdak is called."
    self.a.x = 2
    d = do_(lambda: setattr(self.a, self.name, self.val))

    self.assertNotEqual(self.a.x, self.val)

  def test_do_1(self):
    do_(lambda: setattr(self.a, self.name, self.val))()
    self.assertEqual(self.a.x, self.val)

  def test_do_2(self):
    val2 = 2

    do_(lambda: setattr(self.a, self.name, self.val), lambda:
    do_(lambda: setattr(self.a, "y", val2)))()
    self.assertEqual((self.a.x, self.a.y), (self.val, val2))

class test_given_(t.TestCase):
  def test_given_id(self):
    val = 1
    f = given_(return_)

    self.assertEqual(f(val), val)

  def test_given_recursion(self):
    "Test that tail recursion doesn't stack overflow if it uses lambdak's trampoline system."
    factorial = given_(lambda n, acc = 1:
      acc if n <= 1
      else given_(lambda: factorial.k(n - 1, n * acc)))

    try: factorial(1000, 1)
    except: self.assertTrue(False)
    finally: self.assertTrue(True)

class test_assert_(t.TestCase):
  def test_assert_succeed(self):
    try:
      assert_(True)()
      self.assertTrue(True)
    except:
      self.assertTrue(False)

  def test_assert_fail(self):
    self.assertRaises(AssertionError, assert_(False))

class test_raise_(t.TestCase):
  def setUp(self): self.exn = Exception

  def test_raise_last(self):
    try: raise self.exn
    except: self.assertRaises(self.exn, raise_())

  def test_raise_exn_type(self):
    self.assertRaises(self.exn, raise_(self.exn))

  def test_raise_exn_val(self):
    e = Exception("Bad")
    self.assertRaises(self.exn, raise_(e))

  def test_raise_exn_type_val(self):
    msg = "Bad"
    e = Exception(msg)

    try: raise_(Exception, e)()
    except Exception, ee:
      self.assertEqual(ee.message, msg)
      return

    self.assertTrue(False)

class test_cond_(t.TestCase):
  def test_cond_val(self):
    val = 1
    cond_val = cond_(
      [ (lambda: True, lambda: val),
        (lambda: False, lambda: 2) ],
      None)

    self.assertEqual(cond_val(), val)

  def test_cond_noval(self):
    cond_noval = cond_(
      [ (lambda: False, lambda: 1) ],
      None)

    self.assertEqual(cond_noval(), None)

  def test_cond_return_effect(self):
    "An effect wrapped in a lambdak should be returned from cond_."
    a = A()
    a.x = 1
    attr_name = "x"
    val = 2

    cond_(
      [ (lambda: False, lambda: setattr_(a, attr_name, 0)),
        (lambda: True, lambda: setattr_(a, attr_name, val)) ],
      None,
    return_)()
    self.assertEqual(a.x, val)

class test_import_(t.TestCase):
  def test_import_math(self):
    "Math here is representative of the Python standard library."
    pi_floor = import_("math", lambda _: _.floor(_.pi))
    self.assertEqual(pi_floor(), 3)

class test_try_(t.TestCase):
  def setUp(self): self.a = A()

  def test_try_exn(self):
    val = 1

    try_(lambda: 1 / 0, lambda: setattr(self.a, "x", val))()
    self.assertEqual(self.a.x, val)

  def test_try_noexn(self):
    val = 1
    self.a.x = val

    try_(lambda: 1, lambda: setattr(self.a, "x", 2))()
    self.assertEqual(self.a.x, val)

class test_for_(t.TestCase):
  def setUp(self):
    self.a = A()

  def test_for_act(self):
    vals = (1, 2, 3)

    for_(range(1, 4), lambda _: setattr(self.a, "x%s" % _, _))()
    self.assertEqual((self.a.x1, self.a.x2, self.a.x3), vals)

  def test_for_break(self):
    break_val = 3

    for_(range(1, 5), lambda i:
      break_() if i == break_val
      else setattr(self.a, "x", i))()
    self.assertEqual(self.a.x, break_val - 1)

  def test_for_continue(self):
    skip_val = 3
    xs = []

    for_(range(1, 5), lambda i:
      continue_() if i == skip_val
      else xs.append(i))()
    self.assertFalse(skip_val in xs)

class test_while_(t.TestCase):
  def setUp(self):
    self.a = A()
    self.a.x = 0
    self.inc = lambda x: x + 1

  def test_while_expr(self):
    val = 10

    while_(lambda: self.a.x < val, lambda:
      modattr_(self.a, "x", self.inc))()
    self.assertEqual(self.a.x, val)

  def test_while_break(self):
    break_val = 5

    while_(lambda: True, lambda:
      break_() if self.a.x == break_val
      else modattr_(self.a, "x", self.inc))()
    self.assertEqual(self.a.x, break_val)

  def test_while_continue(self):
    "Should immediately skip to the next iteration of the loop if an object of type `continue_` is returned from any of the lambdaks inside the `while_` lambdak."
    xs = []
    skip_val = 2

    while_(lambda: self.a.x <= 4, lambda:
      modattr_(self.a, "x", self.inc, lambda:
      continue_() if self.a.x == skip_val
      else xs.append(self.a.x)))()
    self.assertFalse(skip_val in xs)

class test_attr_accessors(t.TestCase):
  def setUp(self):
    self.a = A()
    self.attr_name = "x"

  def test_setattr_(self):
    val = 1

    setattr_(self.a, self.attr_name, val)()
    self.assertEqual(self.a.x, val)

  def test_delattr_(self):
    self.a.x = 1

    delattr_(self.a, self.attr_name)()
    self.assertFalse(hasattr(self.a, self.attr_name))

  def test_modattr_(self):
    self.a.x = 1
    def inc(x): return x + 1

    modattr_(self.a, self.attr_name, inc)()
    self.assertEqual(self.a.x, 2)

class test_with_(t.TestCase):
  def setUp(self):
    self.a = A()
    self.a.x = 0

    def incr():
      self.a.x += 1
      yield
      self.a.x += 1
    self.incr = contextmanager(incr)
    self.with_lk = with_(self.incr, lambda: None)

  def test_with_ctx_before(self): self.assertEqual(self.a.x, 0)

  def test_with_ctx_after(self):
    self.with_lk()
    self.assertEqual(self.a.x, 2)

  def test_with_get_nothing(self):
    "If the context manager doesn't bind a value, the handler function shouldn't get an argument."
    try: with_(self.incr, lambda: None)()
    except:
      self.assertTrue(False)
      return

    self.assertTrue(True)

  def test_with_get_val(self):
    "If the context manager binds a value, the handler function should get the value as an argument."
    try: with_(lambda: closing(s.StringIO()), lambda _: None)()
    except:
      self.assertTrue(False)
      return

    self.assertTrue(True)

class test_dict_accessors(t.TestCase):
  def setUp(self):
    self.k, self.v = "x", 1
    self.d = { self.k: self.v }

  def test_assign_(self):
    val = 2

    assign_(self.k, val, self.d)()
    self.assertEqual(self.d[self.k], val)

  def test_get_(self): self.assertEqual(get_(self.k, self.d), self.v)

  def test_del_(self):
    del_(self.k, self.d)()
    self.assertTrue(self.k not in self.d)

  def test_mod_(self):
    def inc(x): return x + 1

    mod_(self.k, inc, self.d)()
    self.assertEqual(self.d[self.k], inc(self.v))

if __name__ == "__main__":
  t.main()

