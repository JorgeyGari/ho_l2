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
        sur = [18, 19, 20, 22, 24, 26, 27, 28]
        self.assertEqual(CSPBusSeats.surrounding(23), sur)

    def test_surrounding_left(self):
        sur = [1, 2, 6, 9, 10]
        self.assertEqual(CSPBusSeats.surrounding(5), sur)

    def test_surrounding_right(self):
        sur = [19, 20, 23, 27, 28]
        self.assertEqual(CSPBusSeats.surrounding(24), sur)

    def test_surrounding_front(self):
        sur = [2, 4, 6, 7, 8]
        self.assertEqual(CSPBusSeats.surrounding(3), sur)

    def test_surrounding_back(self):
        sur = [25, 26, 27, 29, 31]
        self.assertEqual(CSPBusSeats.surrounding(30), sur)

    def test_surrounding_doors(self):
        sur = [13, 14, 18, 21, 22]
        self.assertEqual(CSPBusSeats.surrounding(17), sur)


if __name__ == '__main__':
    unittest.main()
