from constraint import *
import sys


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def get_seats(year, mobility) -> list:
    """Gets the available seats for a student given their year and their mobility"""

    if year == '1':
        seats = seat_type['front']
    else:
        seats = seat_type['back']

    if mobility == 'R':
        return intersection(seats, seat_type['blue'])

    return seats


problem = Problem()

students_path = sys.argv[1]  # Path to the input file "students_XX"
seat_type = {  # Dictionary containing the different types of seats
    'blue': [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20],  # Seats reserved for reduced mobility students
    'front': list(range(1, 17)),  # Seats on the front of the bus
    'back': list(range(17, 33))  # Seats on the back of the bus
}

with open(students_path, 'r') as students:
    line = students.readline()  # Read the first line (first student)
    while line:
        line = line.strip('\n')  # Get rid of the unnecessary newline characters
        data = line.split(',')  # Split the string to obtain a list of the student's characteristics

        problem.addVariable(data[0], get_seats(data[1], data[3]))

        line = students.readline()  # Next line

    students.close()
