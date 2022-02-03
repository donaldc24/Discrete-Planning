import json
from queue import PriorityQueue

# Create class Node to use mainly for keeping track of path
class Node:
    # (x, y) represents coordinates of a cell in the matrix
    # maintain a parent node for the printing path
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))
 
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

# Function to take filename and get json data for graph
def read_json(filename, outName):
    # Global variables
    global graph
    global xI
    global XG
    global out
    global aList

    aList = []
    out = outName
    f = open(filename)
 
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    #Stores json info into global variables
    xI = data['xI']
    XG = data['XG']
    graph = data['G']
 
    # Closing file
    f.close()

# Function to call depending on type of algo
def alg(type):
    if type.upper() == 'BFS':
        forwardSearch(xI, 0)
    if type.upper() == 'DFS':
        forwardSearch(xI, -1)
    if type.upper() == 'ASTAR':
        forwardSearch(xI, 1)

# Function to get neighbors of any point on graph
def getNeighbors(node):
    n = []
    dir = [[-1,0],[1,0],[0,-1],[0,1]]
    i = 0

    # At any point 4 possible neighbors
    while i < 4:
        r = node[0] + dir[i][0]
        c = node[1] + dir[i][1]
        if r >= 0 and c >= 0 and r < len(graph) and c < len(graph[0]):
            n.append([r,c])
        i = i+1
    return n

# Main function for performing forward search
# takes the point and k which reprsents type of algo
def forwardSearch(node, k):
    # Checks if starting point is in XG
    if node in XG:
        visited=[node]
        printResults(visited, "visited")
        print_path(visited, "path")
        return
    # Checks if starting point is on graph 
    if graph[node[0]][node[1]] == 1 or node[0] < 0 or node[1] < 0 or node[0] > len(graph) or node[1] > len(graph[0]):
        print("Starting position not valid")
        return
    
    visited=[]
    visited.append(node)
    parent = dict()
    parent[Node(node[0], node[1])] = None
    check = 0

    # Checks if uses BFS/DFS or Astar algo (k == 1 is astar, else BFS/DFS)
    if k == 1:
        # cost to come
        ctc = 0
        # cost to go
        ctg = 0

        # Create priority queue for astar
        queue=PriorityQueue()
        queue.put((0, node))

        while queue:
            # Pops queue and gets (X, Y) from queue
            s = queue.get()
            s = s[1]

            # Checks if current is in XG and if it is then returns
            if s in XG:
                printResults(visited, "visited")
                return
            # Gets neighbors of current
            neighbors = getNeighbors(s)
        
            # Checks for each neighbor whether is valid or not
            for x in neighbors:
                elem = [x[0], x[1]]
                if elem not in visited and graph[x[0]][x[1]] != 1:
                    # Creates node to then track inside parent dict
                    n = Node(x[0], x[1])
                    parent[n] = s
                    # Checks if current neighbor (elem) is in XG and that this hasnt been true previously
                    # then calls to print path to json file
                    if elem in XG and check == 0:
                        check = 1
                        print_path(parent, Node(elem[0], elem[1]))
                        visited.append(elem)
                    visited.append(elem)
                    # Calculates cost to go and cost to come to use in priority queue
                    ctc = ctc + 1
                    ctg = min((abs(x[0] - XG[0][0]) + abs((x[1] - XG[0][1]))), (abs(x[0] - XG[1][0]) + abs((x[1] - XG[1][1]))))
                    queue.put((ctc+ctg, elem))
    else:
        # Uses normal queue
        queue=[]    
        queue.append(node)
        while queue:
            # Pops queue and gets (X, Y) from queue
            # Either fifo or lifo depending on value of k (0 or -1)
            s = queue.pop(k)

            # Checks if current is in XG to then return
            if s in XG:
                printResults(visited, "visited")
                return
            neighbors = getNeighbors(s)
        
            # Checks for each neighbor whether is valid or not
            for x in neighbors:
                elem = [x[0], x[1]]
                if elem not in visited and graph[x[0]][x[1]] != 1:
                    # Creates node to then track inside parent dict
                    n = Node(x[0], x[1])
                    parent[n] = s
                    # Checks if current neighbor (elem) is in XG and that this hasnt been true previously
                    # then calls to print path to json file
                    if elem in XG and check == 0:
                        check = 1
                        print_path(parent, Node(elem[0], elem[1]))
                        visited.append(elem)
                    visited.append(elem)
                    queue.append(elem)
    print("Can not reach a destinantion")
    return

# Simple function to reverse a list
def Reverse(lst):
    lst.reverse()
    return lst
    
# Is called when path is found
# input path and goal node
# then call printResults
def print_path(p, n):
    path = []
    path.append([n.x, n.y])
    t = p[n]

    # Checks if current is not None
    while t is not None:
        arr = [t[0], t[1]]
        path.append(arr)
        n2 = Node(t[0], t[1])
        t = p[n2]

    printResults(Reverse(path), "path")

# Called for when visited is done and when path is found
# Takes list as input aand string which determines if visited or path list
# Then calls output to write to json file
def printResults(vis, type):
    result = []

    # Reverses the coordinates and puts them in result list
    for i in vis:
        if i[::-1] not in result:
            result.append(i[::-1])

    # Checks for type
    if type == "visited":
        print(result)
        output("visited", result, 0)
    else:
        print(result)
        output("path", result, 1)

# Is called to write to json file
# Input is type, and then a list, and a check
def output(type, result, check):
    vis = []
    path = []

    # Checks to see what type the list is then appends to aList
    if type == "visited":
        vis = result
        aList.append(vis)
    else:
        path = result
        aList.append(path)
    # If Check is 0 then that means both visited and path has been found
    if check == 0:
        makeJson(aList)

# Simple function to write to json file
# takes a list as input
def makeJson(aLis):
    jsonFile = open(out, "w")
    jsonString = json.dumps({"visited": aLis[1], "path": aLis[0]})
    jsonFile.write(jsonString)
    jsonFile.close()

# Inputs, gets filename for graph
# then type of algo
# then lastly the name you want your output file
filename = input("")
algo_name = input("--alg ")
output_file = input("--out ")
rj = read_json(filename, output_file)
a = alg(algo_name)