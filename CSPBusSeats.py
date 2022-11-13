import sys
from constraint import *


def intersection(lst1, lst2) -> list:
    """Returns the intersection of two lists."""
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


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


def main():
    problem = Problem()

    seats = {
        "all": [i for i in range(1, 33)],
        "blue": [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20],  # Seats reserved for reduced mobility students
        "front": [i for i in range(1, 17)],  # Seats on the front of the bus
        "back": [i for i in range(17, 33)]  # Seats on the back of the bus
    }

    students_path = sys.argv[1]  # Path to the input file "students_XX"

    matrix = []

    with open(students_path, 'r') as students:
        line = students.readline()  # Read the first line (first student)
        while line:
            line = line.strip('\n')  # Get rid of the unnecessary newline characters
            data = [int(i) if i.isdigit() else i for i in line.split(',')]  # Split the string to obtain a list of the
            # student's characteristics
            matrix.append(data)
            line = students.readline()  # Next line

        students.close()

    for s in range(0, len(matrix)):
        domain = seats["all"]

        if matrix[s][4] != 0:
            if matrix[matrix[s][4]][1] != matrix[s][1]:     # Siblings in different years
                domain = seats["front"]
        else:
            match matrix[s][1]:
                case 1:
                    domain = seats["front"]
                case 2:
                    domain = seats["back"]

        if matrix[s][3] == "R":
            domain = intersection(domain, seats["blue"])

        problem.addVariable(str(matrix[s][0]), domain)

    # Constraint: Each student has one and only one seat assigned
    problem.addConstraint(AllDifferentConstraint())

    print(problem.getSolutions())


if __name__ == '__main__':
    main()
