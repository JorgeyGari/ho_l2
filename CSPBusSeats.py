import sys

from constraint import *


def intersection(lst1, lst2) -> list:
    """Returns the intersection of two lists."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def bus_zone(s, y) -> bool:
    """Constraint for separating young and older students."""
    if y == '1':
        return s < 17
    return s >= 17


def reduced_mobility(s) -> bool:
    """Constraint for assigning blue seats to reduced mobility students."""
    blue_seats = [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]  # Seats reserved for reduced mobility students
    return s in blue_seats


def adjacent(s1, s2) -> bool:
    """Determines if two seats are adjacent."""
    return abs(s1 - s2) == 1 and (s1 - 1) // 4 == (s2 - 1) // 4


problem = Problem()
seats = [str(i) for i in range(1, 33)]

students_path = sys.argv[1]  # Path to the input file "students_XX"

with open(students_path, 'r') as students:
    line = students.readline()  # Read the first line (first student)
    while line:
        line = line.strip('\n')  # Get rid of the unnecessary newline characters
        data = [int(i) if i.isdigit() else i for i in line.split(',')]  # Split the string to obtain a list of the
        # student's characteristics

        # Naming some variables to improve readability
        st_id = data[0]     # Short for "student ID"
        year = data[1]
        troublesome = data[2]
        mobility = data[3]
        sibling = data[4]

        problem.addVariables(st_id, seats)  # Add this student as a new variable

        problem.addConstraint(st_id, bus_zone(st_id, year))  # Constraint for the zone of the bus (back/front)
        if mobility == 'R':
            problem.addConstraint(st_id, reduced_mobility(st_id))

        line = students.readline()  # Next line

    students.close()
