import unittest as t
from lambdak import *

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
    class A: pass
    a = A()
    val = 1

    do_(setattr(a, "x", val))()
    self.assertEqual(a.x, val)

  def test_do_2(self):
    class A: pass
    a = A()
    (val1, val2) = (1, 2)

    do_(setattr(a, "x", val1), lambda:
    do_(setattr(a, "y", val2)))()
    self.assertEqual((a.x, a.y), (val1, val2))

class test_return_(t.TestCase):
  def test_return_val(self):
    val = 1

    self.assertEqual(return_(val)(), val)

if __name__ == "__main__":
  t.main()

