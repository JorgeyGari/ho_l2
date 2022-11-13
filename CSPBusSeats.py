import sys
from constraint import *


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


problem = Problem()
seats = [str(i) for i in range(1, 33)]

students_path = sys.argv[1]  # Path to the input file "students_XX"


def main():
    with open(students_path, 'r') as students:
        line = students.readline()  # Read the first line (first student)
        while line:
            line = line.strip('\n')  # Get rid of the unnecessary newline characters
            data = [int(i) if i.isdigit() else i for i in line.split(',')]  # Split the string to obtain a list of the
            # student's characteristics

            # Naming some variables to improve readability
            st_id = data[0]  # Short for "student ID"
            year = data[1]
            troublesome = data[2]
            mobility = data[3]
            sibling = data[4]

            problem.addVariable(st_id, seats)  # Add this student as a new variable

            match year:  # Determine zone of the bus depending on the student's school year
                case 1:
                    problem.addConstraint(front, st_id)
                case 2:
                    problem.addConstraint(back, st_id)

            if mobility == 'R':
                problem.addConstraint(reduced_mobility, st_id)

            line = students.readline()  # Next line

        students.close()


if __name__ == '__main__':
    main()
