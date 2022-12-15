import sys
import time
from pathlib import Path

from queue import PriorityQueue


class Node:
    """Each node represents the state of the bus queue when a new student is added at the end."""

    def __init__(self, parent, state=None, cost=0, st_id=0):
        if state is None:
            state = []
        self.children = []
        self.parent = parent
        self.state = state  # Current state of the bus queue (a list of student IDs in order)
        self.cost = cost  # Cost from start node, is zero by default
        self.studentID = st_id  # Student ID of the student that is getting on the bus, is zero by default

        if parent:
            self.path = parent.path[:]
            self.path.append(state)

        else:
            self.path = [state]

    def __lt__(self, other):
        return self.cost < other.cost

    def GetTime(self, student_data) -> int:
        """Get the time that it takes for the student to get on the bus"""

        time = 1  # Default time to get on the bus
        previous_student = self.parent.studentID  # Student in front of the current one

        if student_data[self.studentID][2] == 'R':  # If the current student has reduced mobility
            time = 0  # The student behind will help them get on the bus

        if previous_student == 0:  # If the current student is the first one to get on the bus
            return time

        if student_data[previous_student][2] == 'R':  # If the previous student had reduced mobility
            time *= 3  # The student takes the time needed by the reduced mobility
            if student_data[self.studentID][1] == 'C':
                time *= 2  # Troublesome students take twice as much time to help a reduced mobility student

        if student_data[previous_student][1] == 'C':  # If the previous student was troublesome
            time *= 2  # Double the time to get on the bus

        if student_data[self.studentID][1] == 'C':  # If the current student is troublesome
            time += self.parent.GetTime(student_data)  # Double the time of the previous student

        seated_c = [student_data[i][0] for i in self.state if
                    student_data[i][1] == 'C']  # List of seats taken by troublesome students

        for c in seated_c:
            if student_data[self.studentID][0] > c:  # Time doubles for each troublesome student sitting in front
                time *= 2

        return time

    def CreateChildren(self, student_data):
        remaining_students = [i for i in range(1, len(student_data) + 1) if i not in self.state]

        for student in remaining_students:
            if self.studentID != 0:  # If the node is not the root node
                if student_data[self.studentID][2] == 'R' and student_data[student][2] == 'R':
                    continue  # A reduced mobility student cannot be behind another reduced mobility student

            if student_data[student][2] == 'R' and len(remaining_students) == 1:
                continue  # A reduced mobility student cannot be the last one to get on the bus

            if self.state is None:
                self.state = []
            child = Node(self, self.state + [student], self.cost,
                         student)  # Create the child node corresponding to the new state
            child.cost += child.GetTime(student_data)  # Add the time it takes for the student to get on the bus
            self.children.append(child)  # Add the child to the list of children


class AStarSolver:
    def __init__(self, start, end, student_data, heuristic):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.end = end
        self.student_data = student_data

        match heuristic:
            case '1':
                self.heuristic = self.heuristic1
            case '2':
                self.heuristic = self.heuristic2
            case _:
                print("[ERROR] Please select a heuristic (1 or 2).")

    def heuristic1(self, node) -> int:
        """Heuristic function that returns the number of students that are still waiting to get on the bus."""
        remaining_students = [i for i in range(1, len(self.student_data) + 1) if i not in node.state]
        return len(remaining_students)

    def heuristic2(self, node) -> int:
        """Heuristic function that returns the number of students that are still waiting to get on the bus, with
        the troublesome students having double value."""
        remaining_students = [i for i in range(1, len(self.student_data) + 1) if i not in node.state]
        remaining_students += [i for i in range(1, len(self.student_data) + 1) if
                               i not in node.state and self.student_data[i][1] == 'C']
        return len(remaining_students)

    def Solve(self):
        sol_cost = -1  # Cost of the solution, defaults to -1 in case no solution is found
        start_node = Node(None, None, 0, 0)
        self.priorityQueue.put(
            (0, start_node))  # Add the initial state to the priority queue that will pick out which node to expand

        while not self.path and not self.priorityQueue.empty():  # While there are nodes to expand and no solution
            closest_child = self.priorityQueue.get()[1]  # Get the node with the lowest f cost from the open nodes list
            closest_child.CreateChildren(self.student_data)  # Create the children of the node
            self.visitedQueue.append(closest_child.state)  # Add the state to the visited states list

            for child in closest_child.children:  # For each child of the node
                if child.state not in self.visitedQueue:  # If the child state is not in the visited states list
                    child_priority = child.GetTime(self.student_data) + self.heuristic(
                        child)  # Calculate the priority of the child (function f = g + h)

                    if self.heuristic(child) == 0:  # If the child is a goal
                        self.path = child.path  # Set the path to the child's path
                        sol_cost = child.cost  # Set the solution cost to the child's cost
                        break  # Break out of the loop because we have found a solution

                    self.priorityQueue.put((child_priority, child))  # Add the child to the open nodes list

        return self.path, self.visitedQueue, sol_cost


def studentsDict(students_path) -> dict:
    """Reads the file provided as argument and outputs all the student data in a 2D array."""

    student_data = {}  # Dictionary that will contain all the student data

    with open(students_path, 'r') as students:
        data = []
        line = students.readline()  # The input file must contain exactly one line

        line = line.strip('\n{}')  # Get rid of the new line character and the curly brackets
        line = line.replace(" ", "")  # Get rid of the unnecessary spaces
        line = line.replace("'", "")  # Get rid of the unnecessary quotes
        data += line.split(',')  # Split the line into a list of strings and add it to the data list

        students.close()

    for student in data:
        split = student.split(':')  # Split the student data into student code and assigned seat
        student_data[int(split[0][:-2])] = (int(split[1]), split[0][-2], split[0][
            -1])  # Value is a tuple with the assigned seat, the student's behavior and the student's mobility

    return student_data


def main():
    students_path = sys.argv[1]  # Path to the input file
    students_dict = studentsDict(students_path)
    problem = AStarSolver([], [], studentsDict(students_path), sys.argv[2])
    start_time = time.time()
    sol = problem.Solve()
    end_time = time.time()

# Output the file with the solution
    filename = Path(students_path).with_stem(Path(students_path).stem + "-" + sys.argv[2]).with_suffix('.output')
    with open(filename, 'w') as f:
        if sol[0]:
            f.write("INITIAL: {")

            counter = 0
            for key, value in sorted(students_dict.items(), key=lambda item: item[1][0]):
                counter += 1
                f.write(f"'{key}{value[1]}{value[2]}': {value[0]}")

                if counter != len(students_dict):  # If this is not the student with the highest assigned seat
                    f.write(", ")

            f.write("}\n")

            f.write("FINAL:   {")
            for i in sol[0][-1]:
                f.write(f"'{i}{students_dict[i][1]}{students_dict[i][2]}': {students_dict[i][0]}")
                if i != sol[0][-1][-1]:  # If this is not the last student to get on the bus
                    f.write(", ")

            f.write("}\n")
        else:
            f.write("No solution!")

# Output the file with the execution statistics
    filename = Path(students_path).with_stem(Path(students_path).stem + "-" + sys.argv[2]).with_suffix('.stat')
    with open(filename, 'w') as f:
        f.write(f"Total time: {end_time - start_time}\n")  # Time A* took to find a solution
        if sol:
            f.write(f"Total cost: {sol[2]}\n")  # Cost of the solution
            f.write(f"Plan length: {len(sol[0]) - 1}\n")  # Depth of the solution
            f.write(f"Plan cost: {len(sol[1])}\n")  # Number of nodes expanded before finding the solution
        else:
            f.write(f"No solution!")


if __name__ == '__main__':
    main()
