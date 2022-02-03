# Discrete-Planning
Consider a robot moving on a 2D grid. Each grid point has an integer coordinate
of the form (i, j) where i ∈ {0, . . . , M}, j ∈ {0, . . . , N}, and M and N are positive
integers. The state space is, therefore, defined as
X = {(i, j) ∈ Z × Z | 0 ≤ i ≤ M, 0 ≤ j ≤ N}. (1)
The configuration of the grid is given by a 2D array of the form
G =





O0,0 O1,0 · · · OM,0
O0,1 O1,1 · · · OM,1
.
.
.
.
.
.
.
.
.
.
.
.
O0,N O1,N · · · OM,N





, (2)
where Oi,j ∈ {0, 1} indicates whether cell (i, j) is occupied, i.e., Oi,j = 1 if and only if
cell (i, j) is occupied by an obstacle. Notice that when writing G as a 2-dimensional
list, its indices are such that G[i][j] corresponds to cell (j, i).
The robot takes discrete steps in one of the four directions (up, down, left, right)
with the corresponding actions uup = (0, 1), udown = (0, −1), ulef t = (−1, 0), and
uright = (1, 0). Let U = {uup, udown, ulef t, uright}. The action space for x = (i, j) is
defined as U(x) ⊆ U such that
• uup ∈ U(x) if and only if j < N and Oi,j+1 = 0,
• udown ∈ U(x) if and only if j > 0 and Oi,j−1 = 0,
• ulef t ∈ U(x) if and only if i > 0 and Oi−1,j = 0,
• uright ∈ U(x) if and only if i < M and Oi+1,j = 0.
Task: Implement the 3 variants of forward search algorithm: breadth-first, depth-first,
and A*. The problem description will be provided in a json file, containing the following
fields:
• "G": a 2-dimensional list representing the grid configuration G,
• "xI": a list [i, j] specifying the initial cell xI = (i, j) ∈ X, and
• "XG": a list of [i, j]’s, each corresponding to a goal cell xG ∈ XG ⊂ X.
Your code should take 2 inputs: (1) the algorithm (bfs, dfs, or astar), and (2) the
path to the json file, which specifies the problem description with the above format. It
should output a json file, containing the following fields:
• "visited": the list of visited cells, and
1
• "path": the list of cells specifying the path from xI to XG.
For example, if your code is project1.py, running
python project1.py project1_desc.json --alg bfs --out project1_bfs.json
should output project1 bfs.json, which contains the output of running breadth-first
search, including "visited" and "path" for the problem described in project1 desc.json.
Example of project1 bfs.json and project1 desc.json can be found on the course
github repo.
Requirements:
• To simplify grading, please explore the actions in the following order: uup, udown,
ulef t, uright.
• Do NOT implement each algorithm as a separate function. Instead, you should
implement the general template for forward search (See Figure 2.4 in the textbook).
Then, implement the corresponding priority queue for each algorithm.
Hint: The only difference between different algorithms is how an element is
inserted into the queue. So at the minimum, you should have the following classes:
– Queue: a base class for maintaining a queue, with pop() function that removes
and returns the first element in the queue. You may also want this class to
maintain the parent of each element that has been inserted into the queue so
that you trace back the parent when computing the path from xI to a goal
cell xG ∈ XG.
– QueueBFS, QueueDFS, QueueAstar: classes derived from Queue and implement
insert(x, parent) function for inserting an element x with parent parent
into the queue.
With the above classes, you can implement a general fsearch(G, U, xI, XG,
Q) function, which takes as input the grid configuration G, the list U of actions,
the initial cell xI, the list XG of goal cells, and the queue object Q that contains
insert and pop functions (and possibly some other functions, e.g., for computing
a path).
• Following the previous bullet, there should be only one conditional statement for
the selected algorithm (BFS, DFS or Astar) in the entire program.
• For A*, assume that the cost of each action is 1, i.e., cost-to-come to cell x
0
is given
by C(x
0
) = C(x) + 1 where x is the parent of x
0
. Suppose a state is written as
x = (x
1
, x2
). Use Gˆ∗
(x) = minxG∈XG

|x
1 − x
1
G| + |x
2 − x
2
G|

as the underestimate
of the optimal cost-to-go at x.
• Please feel free to use external libraries, e.g., for heap, queue, stack or implement
them yoursel
