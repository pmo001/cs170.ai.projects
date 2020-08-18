Project 1					CS 170. Introduction to Artificial Intelligence

Paul Mo	
pmo001@ucr.edu
Instructor: Dr. Eamonn Keogh
8-November-2019

In completing this homework, I consulted…

Lorem Ipsum’s sample project. It inspired me to use heapq and copy. I also used the report as a guideline. I also copied his Puzzles 1 to 4 (Puzzle 5 was a duplicate of Puzzle 1).
Project_1_The_Eight_Puzzle briefing as a guideline.
Python 3.8.0 documentation for heapq
https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle (on how to calculate the manhattan distance)
https://www.tutorialspoint.com/python/python_nodes.htm (on how to create my own nodes)
http://benalexkeen.com/bar-charts-in-matplotlib/ as an example on how to produce side-by-side bar graphs

All the important code is original. Unimportant subroutines that are not completely original are…

“heapq”, which is an implementation of the heap queue algorithm. It is available in Python 3.8.0 documentation for heapq.
The ability to deepcopy from “copy”.
numpy for the bar graph representation
matplotlib.plyplot for the bar graph representation

============================================================================================

The following is a trace of the Manhattan distance A* on the following problem:

Enter a 3x3 puzzle. Use a 0 to represent the blank. After each number, enter a space.
Enter the first row: 1 2 3
Enter the second row: 4 0 6
Enter the third row: 7 5 8
Type ‘manhattan’ for Manhattan Distance Heuristic.
Type ‘hamming’ for Hamming Distance Heuristic.
Type ‘uniform cost’ for Uniform Cost Search. manhattan
  
Expanding this state:
[1, 2, 3]
[4, 0, 6]
[7, 5, 8]
g(n) =  0
h(n) =  2
Expanding this state:
[1, 2, 3]
[4, 5, 6]
[7, 0, 8]
g(n) =  1
h(n) =  1
moves: DR
 total # of expanded nodes: 7
max # of nodes in heap:  6

My summary
To solve this problem with A* with the Manhattan Distance heuristic, it required two moves (Down, Right) in order to get to the goal node. In doing so, a total of 7 nodes were expanded. The maximum number of nodes in the queue at any one time was 6.

==========================================================================================

CS170: Project 1 Report
Introduction
This assignment is the first project of Dr. Eamonn Keogh’s Introduction to AI course at the University of California, Riverside during the quarter of Fall 2019. This report will compare the time and space complexities from the application of these three following algorithms to the Eight Puzzle. My programming language of choice was Python (version 3).

Algorithms
Uniform Cost Search
A* with the Hamming Distance heuristic (also called the Misplaced Tile heuristic)
A* with the Manhattan Distance heuristic

Uniform Cost Search
	From the project briefing, this algorithm is just A* with h(n), the heuristic function, hardcoded to 0. The cost of expanding any node is 1 (this also applies to the rest of the project). Thus, g(n), which is the cost from the root node to the current node, will increment by 1 with each node expanded. Essentially, this is like Breadth First Search algorithm, since there is no h(n) value to help the algorithm prioritize which node (level-by-level) to expand.

The Hamming Distance Heuristic (also known as the Misplaced Tile Heuristic)
	This heuristic looks at the number of tiles that are different from the goal state. In my code, I converted my puzzle into a list so that I could compare it to a second list that contains the goal state in order. For example:
The puzzle: 1 2 3 would look like this as a list: [1, 2, 3, 4, 0, 6, 7, 5, 8]
	        4 0 6
	        7 5 8
The goal list would look like: [1, 2, 3, 4, 5, 6, 7, 8, 0]
Each tile that is different from the goal list tile would increment h(n). This includes the 0 tile, (which is the placeholder) as I cannot think of a reason why it needs to be excluded from this specific heuristic. However, if you so desire, you can decrement h(n) by 1 to ignore the 0 case. Overall, both this A* algorithm and the following algorithm will prioritize the lowest h(n) value in its decision of which node to expand.

The Manhattan Distance Heuristic
	In this heuristic, for each tile that is out of place, a value is given to each tile where the value is the minimal number of moves (Up, Down, Left, Right) required for the tile to reach its desired position. Then, it takes the sum of all the values given to each tile (excluding the 0-tile) and assigns it to h(n). Using the example above, tile 5 and tile 8 are misplaced and each take one move to get to their desired position, so h(n) is the sum, which is 2.

Data Analysis

Comparing Uniform Cost Search to the other two A* algorithms w.r.t time:
	Regarding “Table1”, there are blanks for Uniform Cost Search for “Puzzle4” and “Puzzle2” because both take more than 1 hour to produce results (which is also more time required than any other puzzle), and I unfortunately do not have the time to wait for them. This also implicates how the Uniform Cost Search is strictly worse than the other two A* algorithms. “Figure2” provides a visual representation of how grossly time-consuming the Uniform Cost Search is compared to the other two--by comparing the data on the two puzzles that do have complete data: “Puzzle3” and “Puzzle1”. The Uniform Cost Search completely dwarfs the other two A* algorithms.
 
Comparing Uniform Cost Search to the other two A* algorithms w.r.t space:
“Table3” further shows how inferior Uniform Cost search is compared to the A* algorithms. Again, there are two blanks for Uniform Cost Search because both took more time than any other puzzle, which reinforces the fact that Uniform Cost search is strictly worse than the other two A* algorithms.

Comparing the two A* algorithms with each other:
With respect to time complexity:
The more interesting comparison is with the A* algorithms. With respect to puzzles that require only a few moves to get to the goal state (i.e. “must_trace”, “Puzzle3”), the distinctions between the A* algorithms are minimal. This is visually represented in “Figure4”; they get to the solution with the minimal of moves. However, once we approach complicated puzzles that require significantly more moves, the rift between the A* algorithms grows more apparent. 
In terms of time complexity, the Manhattan Distance heuristic seems to grow linearly and at a slower pace. This can be seen in “Figure4” where the blue bars seem to plateau. On the other hand, in the same figure, the Hamming Distance heuristic seems to grow at an exponential rate as the puzzle gets more complex. 

With respect to space complexity:
With respect to the maximum queue size, the results align with the results from the comparison with respect to time complexity. In “Figure5”, the Manhattan Distance heuristic’s blue bars appear to grow linearly and almost plateau like logarithmic growth as the complexity of the puzzles grow. However, the Hamming Distance heuristic grows exponentially like it did for the time complexity comparison in “Figure4”.

Conclusion
Without a doubt, the Uniform Cost Search is strictly worse than the A* algorithms in both time complexity and space complexity. 
On the other hand, the A* with Manhattan Distance heuristic is strictly better than the other two algorithms. This heuristic expanded the least number of nodes by a large margin, which means that it is the best in time complexity compared to the other two. Furthermore, the A* with Manhattan Distance heuristic also has the least number of maximum nodes in the queue, which means this is the best in space complexity compared to the other two. 
For this 8-puzzle problem, the A* with Manhattan Distance heuristic is the best algorithm and it should be the only algorithm worth considering for this problem. Even though A*, in general, has the reputation of being the best, its heuristic is what defines the algorithm.
