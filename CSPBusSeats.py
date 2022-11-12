from constraint import *
import sys


def intersection(lst1, lst2) -> list:
    """Returns the intersection of two lists."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def siblings(s1, s2) -> bool:
    """Constraint for two siblings who must sit together."""
    return True


def bus_zone(s, year) -> bool:
    if year == '1':
        return s < 17
    return s >= 17


def reduced_mobility(s) -> bool:
    blue_seats = [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]  # Seats reserved for reduced mobility students
    return s in blue_seats


def adjacent(s1, s2) -> bool:
    return abs(s1 - s2) == 1 and (s1 - 1) // 4 == (s2 - 1) // 4


problem = Problem()
seats = [str(i) for i in range(1, 33)]

students_path = sys.argv[1]  # Path to the input file "students_XX"

with open(students_path, 'r') as students:
    line = students.readline()  # Read the first line (first student)
    while line:
        line = line.strip('\n')     # Get rid of the unnecessary newline characters
        data = [int(i) if i.isdigit() else i for i in line.split(',')]
        # Split the string to obtain a list of the student's characteristics

        id = data[0]
        year = data[1]
        troublesome = data[2]
        mobility = data[3]
        sibling = data[4]

        problem.addVariables(id, seats)

        problem.addConstraint(id, bus_zone(id, year))  # Constraint for the zone of the bus (back/front)
        if mobility == 'R':
            problem.addConstraint(id, reduced_mobility(id))

        line = students.readline()  # Next line

    students.close()
