import unittest as t
import lambdak as l

class test_lambdak(t.TestCase):
  def test_init_k_x(self):
    args = (1, 2)
    lk = l.lambdak(*args)

    self.assertEqual((lk.k, lk.x), args)

  def test_init_k(self):
    lk = l.lambdak(1)

    self.assertEqual((lk.k, lk.x), (1, None))

if __name__ == "__main__":
  t.main()

