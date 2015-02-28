import unittest
import hw1

class hw1_test(unittest.TestCase):
  def test_parse(self):
    self.assertEqual(
        hw1.parse('0 1 3\n4 2 5\n7 8 6'),
        ((0,1,3),(4,2,5),(7,8,6)))
    with self.assertRaises(ValueError):
      hw1.parse('0 1 3\n4 2 5\n7 8')
    with self.assertRaises(ValueError):
      hw1.parse('0 1 3\n4 2 5\n7 6 6')
    with self.assertRaises(ValueError):
      hw1.parse('0 1 3\n4 2 5\n7 8 9 10')

  def test_neighbors(self):
    self.assertCountEqual(
        hw1.neighbors(((0,1,3),(4,2,5),(7,8,6))),
        (
          ((1,0,3),(4,2,5),(7,8,6)),
          ((4,1,3),(0,2,5),(7,8,6)),
        ))
    self.assertCountEqual(
        hw1.neighbors(((1,2,3),(4,0,5),(7,8,6))),
        [
          ((1,0,3),(4,2,5),(7,8,6)),
          ((1,2,3),(0,4,5),(7,8,6)),
          ((1,2,3),(4,5,0),(7,8,6)),
          ((1,2,3),(4,8,5),(7,0,6)),
        ])

  def test_distance(self):
    self.assertEqual(
        hw1.distance(((0,1,3),(4,2,5),(7,8,6))),
        4)
    self.assertEqual(
        hw1.distance(((1,2,3),(4,5,6),(7,8,0))),
        0)

  def test_find_path(self):
    start = ((0,1,3),(4,2,5),(7,8,6))
    expected_path = [
      ((0,1,3),(4,2,5),(7,8,6)),
      ((1,0,3),(4,2,5),(7,8,6)),
      ((1,2,3),(4,0,5),(7,8,6)),
      ((1,2,3),(4,5,0),(7,8,6)),
      ((1,2,3),(4,5,6),(7,8,0)),
    ]
    self.assertEqual(
        hw1.find_path(start),
        expected_path)

if __name__=='__main__':
  unittest.main()
