Lab assignment 2 for the course Heuristics and Optimization, imparted by Universidad Carlos III de Madrid in Fall 2022. Coded by Laura Belizón Merchán and Jorge Lázaro Ruiz.

Seat assignment constraint satisfaction problem using the library `python-constraint`. Queue position assignment search problem and implementation of the A* algorithm to solve it.

If you are a student who's been assigned this practice as well, please DO NOT copy our code. Only use it for guidance. We uploaded our work to make future students' lives easier.

# Test cases for Part 1
Here is an overview of what each test case `studentsXX` represents:
* **students01**: Example case provided in the statement
* **students02**: Case where there are too many reduced mobility students
* **students03**: Case with more than three siblings from the same family
* **students04**: Case with eight (maximum) troublesome students
* **students05**: Case with one single student who can sit on the front
* **students06**: Case with six (maximum) reduced mobility students
* **students07**: Case with nine troublesome students (exceeds maximum)

# Test cases for Part 2
Here is an overview of what each test case `studentsXX.prob` represents:
* **students01.prob**: Example case provided in the statement
* **students02.prob**: Case where all students are reduced mobility students with no one to help them get on the bus
* **students03.prob**: Case where each student with reduced mobility has another student to help them get on the bus
* **students04.prob**: Case where there are no reduced mobility students or troublesome students
* **students05.prob**: Case where all students are troublesome students but there are no reduced mobility students
* **students06.prob**: Case where there is only one troublesome student and one reduced mobility student among other students
* **students07.prob**: Case where there are only two students and one of them has reduced mobility
* **students08.prob**: Case where there are only two students and one of them is troublesome and sits in front of the other one
* **students09.prob**: Case where there are only two students and one of them is troublesome and sits behind the other one
