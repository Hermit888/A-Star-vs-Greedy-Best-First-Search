import sys, os, time, csv
# python path_finding.py GOAL INIT
# python path_finding.py NY OR
# start time
timeStart = time.time()

# determine whether there is enough or too many inputs
if len(sys.argv) != 3:
    print('Not enough or too many input arguments')
    sys.exit()

goal = sys.argv[1]
initial = sys.argv[2]

# determine whether input is not in data
with open('driving.csv', 'r') as csvfile:
    for row in csv.reader(csvfile):
        if (goal not in row) or (initial not in row):
            timeEnd = time.time()
            elapsedTimeInSec = timeEnd - timeStart
            print('Solution: NO SOLUTION FOUND\
                \nNumber of stops on a path: 0\
                \nExecution time:' + str(elapsedTimeInSec) + '\
                \nComplete path cost: 0')
            sys.exit()
        break



#### greedy best first search
def expand(node):
    with open('driving.csv', 'r') as csvfile:
        for row in csv.DictReader(csvfile): 
            if row['STATE'] == node:
                child = dict()
                for k, v in row.items():
                    if k != 'STATE' and int(v) != -1 and k != node:
                        child[k] = int(v)
                
                return child


def sortNode(lst, goal):
    nodeWiVal = dict()
    for node in lst:
        with open('straightline.csv', 'r') as csvfile:
            for row in csv.DictReader(csvfile):
                if row['STATE'] == node:
                    nodeWiVal[node] = int(row[goal])
    
    sorted_nodes = sorted(nodeWiVal.items(), key = lambda x:x[1])
    newLst = []
    for i in sorted_nodes:
        newLst.append(i[0])
    return newLst


def gbfs(initial, goal):
    path = []
    frontier = [initial]
    reached = {initial: 0}
    num_expanded = 0

    while frontier:
        node = frontier.pop(0)
        
        if node == goal:
            return path + [node], reached[node], num_expanded
        
        nodes = []
        for k, v in expand(node).items():
            if k not in reached or reached[node] + v < reached[k]:
                reached[k] = reached[node] + v
                nodes.append(k)
        
        if nodes != []:
            num_expanded += 1
            path.append(node)
            frontier = sortNode(nodes, goal) + frontier

    return False

gbfsresult = gbfs(initial, goal)


##### determine whether there's a path 
if not gbfsresult:
    timeEnd = time.time()
    gbfsTime = timeEnd - timeStart
    print('Solution: NO SOLUTION FOUND\
	    \nNumber of stops on a path: 0\
	    \nExecution time:' + gbfsTime + '\
	    \nComplete path cost: 0')
    sys.eixt()
else:
    timeEnd = time.time()
    gbfsTime = timeEnd - timeStart




#### A* search
timeStart = time.time()

def sortNode2(nodes, front):
    newNodes = []
    for parent, node, cost in nodes:
        with open ('straightline.csv', 'r') as csvfile:
            for row in csv.DictReader(csvfile):
                if row['STATE'] == parent:
                    newNodes.append((parent, node, cost + int(row[goal])))
    
    newLst = newNodes + front
    return sorted(newLst, key = lambda x:x[2])

def AStar(initial, goal):
    path = []
    frontier = [(None, initial, 0)]
    reached = {initial: 0}
    num_expanded = 0

    while frontier:
        node = frontier.pop(0)
        
        if node[1] == goal:
            # reverse to find the true path
            path.reverse()
            
            # sol is true path, front is the last stop
            sol = [goal]
            front = node[0]

            for i in path:
                if i[1] == front:
                    sol.append(i[1])
                    front = i[0]

            # sol is reversed path, so reverse back
            sol.reverse()
            return sol, reached[node[1]], num_expanded
        
        nodes = []
        for k, v in expand(node[1]).items():
            if k not in reached or reached[node[1]] + v < reached[k]:
                reached[k] = reached[node[1]] + v
                nodes.append((node[1], k, reached[k]))
        
        if nodes != []:
            num_expanded += 1
            
            # store node's parent and child
            path.append((node[0], node[1]))
            
            frontier = sortNode2(nodes, frontier)

    return False



AstarResult = AStar(initial, goal)
timeEnd = time.time()
AstarTime = timeEnd - timeStart



#### print results
print('Initial state: ' + initial + '\
    \nGoal state: ' + goal)

finalPath = ', '.join(str(i) for i in gbfsresult[0])
print('\nGreedy Best First Search: \
    \nSolution: ' + finalPath + '\
    \nNumber of expanded nodes: ' + str(gbfsresult[2]) + '\
    \nNumber of stops on a path: ' + str(len(gbfsresult[0])) + '\
    \nExecution time: ' + str(gbfsTime) + '\
    \nComplete path cost:' + str(gbfsresult[1]))

finalPath = ', '.join(str(i) for i in AstarResult[0])
print('\nA* Search: \
    \nSolution: ' + finalPath + '\
    \nNumber of expanded nodes: ' + str(AstarResult[2]) + '\
    \nNumber of stops on a path: ' + str(len(AstarResult[0])) + '\
    \nExecution time: ' + str(AstarTime) +'\
    \nComplete path cost: ' + str(AstarResult[1]))