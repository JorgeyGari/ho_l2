import unittest
import CSPBusSeats


class Adjacent(unittest.TestCase):
    def test_adjacent_window(self):
        self.assertEqual(CSPBusSeats.adjacent(9, 10), True)
        self.assertEqual(CSPBusSeats.adjacent(9, 8), False)

        self.assertEqual(CSPBusSeats.adjacent(8, 7), True)

    def test_adjacent_aisle(self):
        self.assertEqual(CSPBusSeats.adjacent(26, 25), True)
        self.assertEqual(CSPBusSeats.adjacent(26, 27), False)

        self.assertEqual(CSPBusSeats.adjacent(27, 28), True)


class Surrounding(unittest.TestCase):
    def test_surrounding_base(self):
        surr = [18, 19, 20, 22, 24, 26, 27, 28]
        self.assertEqual(CSPBusSeats.surrounding(23), surr)

    def test_surrounding_left(self):
        surr = [1, 2, 6, 9, 10]
        self.assertEqual(CSPBusSeats.surrounding(5), surr)

    def test_surrounding_right(self):
        surr = [19, 20, 23, 27, 28]
        self.assertEqual(CSPBusSeats.surrounding(24), surr)

    def test_surrounding_front(self):
        surr = [2, 4, 6, 7, 8]
        self.assertEqual(CSPBusSeats.surrounding(3), surr)

    def test_surrounding_back(self):
        surr = [25, 26, 27, 29, 31]
        self.assertEqual(CSPBusSeats.surrounding(30), surr)


if __name__ == '__main__':
    unittest.main()
