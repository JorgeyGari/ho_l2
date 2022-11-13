import unittest


# FIXME: I can't import CSPBusSeats.py, so, for now, I will just copy and paste the functions
def intersection(lst1, lst2) -> list:
    """Returns the intersection of two lists."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def front(s) -> bool:
    """Constraint for students sitting in the back of the bus."""
    return s < 17


def back(s) -> bool:
    """Constraint for students sitting in the back of the bus."""
    return s > 16


def reduced_mobility(s) -> bool:
    """Constraint for assigning blue seats to reduced mobility students."""
    blue_seats = [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]  # Seats reserved for reduced mobility students
    return s in blue_seats


def adjacent(s1, s2) -> bool:
    """Determines if two seats are adjacent."""
    return abs(s1 - s2) == 1 and (s1 - 1) // 4 == (s2 - 1) // 4 and (s1 % 4) * (s2 % 4) != 6


def same_row(s1, s2) -> bool:
    """Determines if two seats are in the same row."""
    return (s1 - 1) // 4 == (s2 - 1) // 4


def surrounding(s) -> list:
    """Returns a list of all seats surrounding the given seat."""
    sur = []

    if (s - 1) // 4 > 0:  # Check the seat is not in the first row
        if same_row(s - 4, s - 5):
            sur.append(s - 5)  # Add seat in the front-left diagonal
        sur.append(s - 4)  # Add seat in front
        if same_row(s - 4, s - 3):
            sur.append(s - 3)  # Add seat in the front-right diagonal

    if same_row(s, s - 1):
        sur.append(s - 1)  # Add seat to the left

    if same_row(s, s + 1):
        sur.append(s + 1)  # Add seat to the right

    if (s - 1) // 4 < 7:  # Check the seat is not in the last row
        if same_row(s + 4, s + 5):
            sur.append(s + 5)  # Add seat in the back-left diagonal
        sur.append(s + 4)  # Add seat behind
        if same_row(s + 4, s + 3):
            sur.append(s + 3)  # Add seat in the back-right diagonal

    return sur


class Adjacent(unittest.TestCase):
    def test_adjacent_window(self):
        self.assertEqual(adjacent(9, 10), True)
        self.assertEqual(adjacent(9, 8), False)

        self.assertEqual(adjacent(8, 7), True)

    def test_adjacent_aisle(self):
        self.assertEqual(adjacent(26, 25), True)
        self.assertEqual(adjacent(26, 27), False)

        self.assertEqual(adjacent(27, 28), True)


class Surrounding(unittest.TestCase):
    def test_surrounding_base(self):
        surr = [18, 19, 20, 22, 24, 26, 27, 28]
        self.assertEqual(surrounding(23), surr)

    def test_surrounding_left(self):
        surr = [1, 2, 6, 9, 10]
        self.assertEqual(surrounding(5), surr)

    def test_surrounding_right(self):
        surr = [19, 20, 23, 27, 28]
        self.assertEqual(surrounding(24), surr)

    def test_surrounding_front(self):
        surr = [2, 4, 6, 7, 8]
        self.assertEqual(surrounding(3), surr)

    def test_surrounding_back(self):
        surr = [25, 26, 27, 29, 31]
        self.assertEqual(surrounding(30), surr)


if __name__ == '__main__':
    unittest.main()
