import unittest as t
from lambdak import *

# A helper class to test attribute access.
class A: pass

class test_lambdak(t.TestCase):
  def test_init_k_x(self):
    args = (1, 2)
    lk = lambdak(*args)

    self.assertEqual((lk.k, lk.x), args)

  def test_init_k(self):
    lk = lambdak(1)

    self.assertEqual((lk.k, lk.x), (1, None))

class test_do_(t.TestCase):
  def test_do_1(self):
    a = A()
    val = 1

    do_(setattr(a, "x", val))()
    self.assertEqual(a.x, val)

  def test_do_2(self):
    a = A()
    (val1, val2) = (1, 2)

    do_(setattr(a, "x", val1), lambda:
    do_(setattr(a, "y", val2)))()
    self.assertEqual((a.x, a.y), (val1, val2))

class test_let_(t.TestCase):
  def test_let_val(self):
    val = 1
    test_l = let_(val, lambda x: x)

    self.assertEqual(test_l(), val)

class test_assert_(t.TestCase):
  def test_assert_succeed(self):
    try:
      assert_(True)()
      self.assertTrue(True)
    except:
      self.assertTrue(False)

  def test_assert_fail(self):
    try:
      assert_(False)()
      self.assertTrue(False)
    except:
      self.assertTrue(True)

class test_raise_(t.TestCase):
  def test_raise_last(self):
    try: raise Exception
    except:
      try: raise_()
      except Exception:
        self.assertTrue(True)
        return

      self.assertTrue(False)

  def test_raise_exn_type(self):
    try: raise_(Exception)
    except Exception:
      self.assertTrue(True)
      return

    self.assertTrue(False)

  def test_raise_exn_val(self):
    e = Exception("Bad")

    try: raise_(e)
    except Exception:
      self.assertTrue(True)
      return

    self.assertTrue(False)

  def test_raise_exn_type_val(self):
    msg = "Bad"
    e = Exception(msg)

    try: raise_(Exception, e)
    except Exception, ee:
      self.assertEqual(ee.message, msg)
      return

    self.assertTrue(False)

class test_if_(t.TestCase):
  def test_if_then(self):
    val = 1
    then_val = if_(True, lambda: val)

    self.assertEqual(then_val(), val)

  def test_if_else(self):
    val = 1
    else_val = if_(False, None, lambda: val)

    self.assertEqual(else_val(), val)

class test_cond_(t.TestCase):
  def test_cond_val(self):
    val = 1
    cond_val = cond_(
      [ (lambda: True, lambda: val),
        (lambda: False, lambda: 2) ])

    self.assertEqual(cond_val(), val)

  def test_cond_noval(self):
    cond_noval = cond_(
      [ (lambda: False, lambda: 1) ])

    self.assertEqual(cond_noval(), None)

class test_import_(t.TestCase):
  def test_import_math(self):
    "Math here is representative of the Python standard library."
    pi_floor = import_("math", lambda m: m.floor(m.pi))

    self.assertEqual(pi_floor(), 3)

class test_try_(t.TestCase):
  def test_try_exn(self):
    a = A()
    val = 1

    try_(lambda: 1 / 0, lambda: setattr(a, "x", val))()
    self.assertEqual(a.x, val)

  def test_try_noexn(self):
    a = A()
    val = 1
    a.x = val

    try_(lambda: 1, lambda: setattr(a, "x", 2))()
    self.assertEqual(a.x, val)

class test_for_(t.TestCase):
  def test_for_act(self):
    a = A()
    vals = (1, 2, 3)

    for_(range(1, 4), lambda x: setattr(a, "x%s" % x, x))()

    self.assertEqual((a.x1, a.x2, a.x3), vals)

class test_attr_accessors(t.TestCase):
  def test_setattr_(self):
    a = A()
    val = 1

    setattr_(a, "x", val)()
    self.assertEqual(a.x, val)

  def test_delattr_(self):
    a = A()
    attr_name = "x"
    a.x = 1

    delattr_(a, attr_name)()
    self.assertFalse(hasattr(a, attr_name))

if __name__ == "__main__":
  t.main()

