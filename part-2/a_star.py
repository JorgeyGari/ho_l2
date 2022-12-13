import sys
from queue import PriorityQueue

NUM_STUDENTS = 8  # For testing purposes


class Node:
    """Each node represents the state of the bus queue when a new student is added at the end."""

    def __init__(self, parent, state, cost=0, st_id=0):
        self.children = []
        self.parent = parent
        self.state = state  # Current state of the bus queue (a list of student IDs in order)
        self.cost = cost  # Cost from start node, is zero by default
        self.studentID = st_id  # Student ID of the student that is getting on the bus, is zero by default
        if parent:
            self.path = parent.path[:]
            self.path.append(state)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [state]

    def GetTime(self, matrix) -> int:
        """Get the time that it takes for the student to get on the bus"""
        time = 1  # Default time to get on the bus
        previousStudent = self.parent.studentID

        if matrix[(self.studentID - 1)][3] == 'R':  # If the current student has reduced mobility
            time *= 3  # They take three times as much time to get on the bus

        if matrix[(previousStudent - 1)][3] == 'R':  # If the previous student had reduced mobility
            time = 0  # The student already got on the bus while helping the student in front

        if matrix[(previousStudent - 1)][2] == 'C':  # If the previous student was troublesome
            time *= 2  # Double the time to get on the bus

        if matrix[(self.studentID - 1)][2] == 'C':  # If the current student is troublesome
            time += self.parent.GetTime(matrix)  # Double the time of the previous student

        # TODO: Añadir restricción 5

        return time

    def CreateChildren(self, matrix):
        remaining_students = [i for i in range(1, NUM_STUDENTS + 1) if i not in self.state]
        for student in remaining_students:
            if matrix[(self.studentID - 1)][3] == 'R' and matrix[student][3] == 'R':
                continue  # A reduced mobility student cannot be behind another reduced mobility student
            if matrix[student][3] == 'R' and len(remaining_students) == 1:
                continue
            newState = self.state.append(student)
            child = Node(self, newState, self.cost, student)
            child.cost += child.GetTime(matrix)
            self.children.append(child)


class AStar_Solver:
    def __init__(self, start, end, matrix, heuristic):
        self.path = []
        self.visitedQueue = []
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.end = end
        self.matrix = matrix
        if heuristic == 1:
            self.heuristic = self.heuristic1
        else:
            self.heuristic = self.heuristic2

    def heuristic1(self, node) -> int:
        """Heuristic function that returns the number of students that are still waiting to get on the bus."""
        remaining_students = [i for i in range(1, NUM_STUDENTS + 1) if i not in node.state]
        return len(remaining_students)

    def heuristic2(self, node) -> int:
        pass

    def Solve(self):
        startNode = Node(self.start, 0, self.start, self.end)  # The initial state of our bus queue (empty)
        self.priorityQueue.put(
            (0, startNode))  # Add the initial state to the priority queue that will pick out which node to expand
        while not self.path and not self.priorityQueue.empty():  # While we haven't found a solution and there are still nodes to expand
            closestChild = self.priorityQueue.get()  # Get the node with the lowest f cost from the open nodes list
            closestChild.CreateChildren()  # Create the children of the node
            self.visitedQueue.append(closestChild.state)  # Add the state to the visited states list
            for child in closestChild.children:  # For each child of the node
                if child.state not in self.visitedQueue:  # If the child state is not in the visited states list
                    child.priority = child.GetTime(self.matrix) + self.heuristic(
                        child)  # Calculate the priority of the child (function f = g + h)
                    if self.heuristic(child) == 0:  # if child is goal
                        self.path = child.path  # Set the path to the child's path
                        break  # Break out of the loop because we have found a solution
                    self.priorityQueue.put((child.priority, child))  # Add the child to the open nodes list
        if not self.path:
            print("Goal of " + self.end + " is not possible!")
        return self.path


def studentsMatrix(students_path) -> list:
    """Reads the file provided as argument and outputs all the student data in a 2D array."""

    matrix = []  # This will be a 2D array holding the characteristics of each student

    with open(students_path, 'r') as students:
        line = students.readline()  # Read the first line (first student)
        while line:
            line = line.strip('\n')  # Get rid of the unnecessary newline characters
            data = [int(i) if i.isdigit() else i for i in line.split(',')]  # Split the string to obtain a list of the
            # student's characteristics
            matrix.append(data)
            line = students.readline()  # Next line

        students.close()

    return matrix


def main():
    students_path = sys.argv[1]  # Path to the input file
    studentsMatrix(students_path)  # Read the file and store the data in a matrix
