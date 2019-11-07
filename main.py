import heapq #ref: inspired from Lorem Ipsum project sample
import copy #ref: also inspired from sample project

#general srch alg: (from project briefing)
#arg1: problem(init state)
#arg2: queueing-function
#function srch_1,2or3(arg1, arg2):
#nodes = create the node:init state
#  then enqueue init node as root in minheap 
#loop do
#   if init state not valid(empty or impossible), return "failure"
#   if state == goal, return (node?)

trivial = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

#          00  01  02
one_away = [[1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]]
#          20  21  22

must_trace = [[1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]]
            #sol = 2

center = [[1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]]

#value: the key's index position w.r.t matrices   
goal_dict = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2],
            7:[2,0], 8:[2,1]}

#a list of tuples of moves the 0 can do in a matrix
add_move = [('L', (0,-1)),
            ('R', (0, 1)),
            ('U', (-1,0)), 
            ('D', (1,0))]

#global variables
global_heuristic = ""
global_numNodes = 0
global_max_q_len = 0

#fixme: for now, have it set as manhattan
global_heuristic = "manhattan"
#technically, uniform cost isn't a heuristic
#this list is used for def goal_test
list_heuristic = ["manhattan", "hamming"]

def set_heuristic(userInput):
    global_heuristic = userInput
    return


#ref: consulted https://www.tutorialspoint.com/python/python_nodes.htm
#       on how to build node class
#creating nodes class that rep puzl matrices and f_val = g + h
#not a linked list anymore since removed parent and next pointers
class puzl_node:
    def __init__(self, mtx, g_val=0, h_val=0, newMoves=''):
        self.mtx = copy.deepcopy(mtx) #deep copies the mtx(list)
        self.g_val = g_val
        self.h_val = h_val
        self.f_val = self.g_val + self.h_val
        self.zero_pos = locate_zero_pos(self.mtx)
        
        self.storedMoves = newMoves

def print_mtx(mtx):
    for i in range(len(mtx)):
        print(mtx[i])
    return

#to call: arg = node
#purpose: prints node's mtx with g, h, values
def print_nodes_mtx(node):
    for i in range(len(node.mtx)):
        print(node.mtx[i])
    print("g: ", node.g_val)
    print("h: ", node.h_val)
    print("f: ", node.f_val)
    return

#returns a tuple of the position where 0 is
def locate_zero_pos(mtx):
    for y in range(len(mtx)):
        for x in range(len(mtx[0])):
            if mtx[y][x] == 0:
                return (y,x)

#to call this, 1st arg: node
#2nd arg: minheap
#TODO: make it so that I can add each new node made in the for loop to the minheap
def add_poss_mtx_nodes(minheap, node):
    #fixme: change if to for
    
    print("within poss_mtx_node; printing orig mtx:")
    print_mtx(node.mtx)
    print("g(n) = ", node.g_val)
    print("h(n) = ", node.h_val)
    #tuple unpacking of the ordered list: add_move
    for move, add_position in add_move:
        #unpacking the addition of the tuples
        new_y_zero_pos = (node.zero_pos)[0] + add_position[0]
        new_x_zero_pos = (node.zero_pos)[1] + add_position[1]
        
        #skips for loop if out of bounds
        if (new_y_zero_pos > (len(node.mtx)-1) or new_y_zero_pos < 0 or 
            new_x_zero_pos > (len(node.mtx)-1) or new_x_zero_pos < 0):
            continue

        new_mtx = copy.deepcopy(node.mtx)
        tmp_val = new_mtx[new_y_zero_pos][new_x_zero_pos] 
        new_mtx[new_y_zero_pos][new_x_zero_pos] = 0 #moving zero to new pos
        #moving tmp_val to old zero pos
        new_mtx[(node.zero_pos)[0]][(node.zero_pos)[1]] = tmp_val

#todo: set the nodes for the other two
#the only thing that would change would be the if() and the calc_
        if (global_heuristic == "manhattan"):
            new_mtx_node = puzl_node(new_mtx, 
                                        (node.g_val)+1,
                                        calc_h_manhattan_dist(new_mtx),
                                        (node.storedMoves + move))
                        #fixme? rm'd this     (new_y_zero_pos, new_x_zero_pos))
            #assign parent pointer to prev
            new_mtx_node.parent = node #fixme? might not need this with storedMoves
            ##fixme: rm'd: new_mtx_node.numNodes += 1

            #only set global when requires change (i.e increment)
            global global_numNodes
            global_numNodes += 1
            
            #adds move to storedMoves
            #fixme?probnot: rm'd: new_mtx_node.storedMoves += move
            #>>add the new node to minheap (still within if-statement)
            #add to minheap by priority(f-val)
            f = new_mtx_node.f_val
            #heapq will compare the first el of the tuple: f
            #if f are same, will compare numNodes next(the order they are created)
            heapq.heappush(minheap, (f, global_numNodes, new_mtx_node))

            global global_max_q_len
            if global_max_q_len < len(minheap):
                global_max_q_len = len(minheap)
        #print_nodes_mtx(new_mtx_node)
    return

#checks if minheap is empty
def heap_is_empty(minheap):
    return len(minheap) == 0



#arg: init_node = a node from main()
def a_star(init_node):
    minheap = [] #init minheap
    #2nd arg: a tuple of f(n) and the deepcopied mtx
    f = init_node.f_val
    #heapq will compare first el of tuple: f, then numNodes
    heapq.heappush(minheap, (f, global_numNodes, init_node))
    seen = [] #init seen as empty list

    while (not heap_is_empty(minheap)):
        #pops root: a tuple of 0.f_val ; 1.numNodes count 2.node
        popped_node = heapq.heappop(minheap)[2]
        ###print("printing popped node's matrix:   ", popped_node.mtx)
        #ignores repeated states
        #compares lists of the mtx in seen
        if popped_node.mtx in seen:
            continue 
        #if reach goal
        if goal_test(popped_node):
            return (popped_node.storedMoves, global_numNodes)

        #adds mtx(list) into seen, not the entire node
        seen.append(popped_node.mtx)
        #insert new nodes extended from popped
        add_poss_mtx_nodes(minheap, popped_node)
        #all poss new nodes in minheap as of now

            #todo: then start a minheap with newly taken out node?
    return

#TODO: impl. print path from goal state back up to root using parent var

#h(n) = heuristic that /underestimates/
#   the sum of /each/ tile's_distance_to_desired_pos
#purpose: add this with g(n)=cost_of_path2currNode
#   g+h = f, use f to determine which node to expand
def calc_h_manhattan_dist(puzl_list):
    sum = 0
    for y in range(len(puzl_list)): #rowNum 0,1,2
        for x in range(len(puzl_list[0])):
            if puzl_list[y][x] != 0: #0 has no dict
                yIndx_of_goal, xIndx_of_goal = goal_dict.get(puzl_list[y][x])
# ref: https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
# abs(xIndx - xIndx_of_goal) + abs(yIndx - yIndx_of_goal) 
                sum += abs(yIndx_of_goal - y) + abs(xIndx_of_goal - x)
    return sum

def calc_hamming_dist(puzl_list):
    sum = 0
    list1 = []
    for y in range(len(puzl_list)):
        for x in range(len(puzl_list)):
            list1.append(puzl_list[y][x])
    print(list1)
    list2 = [1,2,3,4,5,6,7,8,0]
    for i in range(len(list2)):
        if list1[i] != list2[i]:
            sum += 1
    return sum

#1.if heuristic == manhattan, goal == if h(n) == 0
# if heuristic == hamming, goal == if h(n) == 0
#2.if using uniform cost fcn: must check if each tile is in correct place
def goal_test(node):
    if ((global_heuristic in list_heuristic) and node.h_val == 0):
        return True
    elif global_heuristic == "uniform cost" and equal_trivial(node.mtx):
        return True
    else:
        return False

#compares arg_mtx with trivial: tile by tile
def equal_trivial(mtx):
    for y in range(len(trivial)):
        for x in range(len(trivial[0])):
            if mtx[y][x] != trivial[y][x]:
                return False
    return True


#TODO: set global_heuristic = "manhattan" or whatever user wants
global_heuristic = "manhattan" #fixme later
def main():
#tests:
    #1st arg: mtx, 2nd arg: g, 3rd arg: h, 4th:zero_pos
    ####mtx_node = puzl_node(one_away, 0, calc_h_manhattan_dist(one_away))

    #set as global so that this global variable can be changed
    global global_numNodes
    global global_max_q_len
#    global_numNodes = 0
#    global_max_q_len = 0
#    mtx_node = puzl_node(center, 0, calc_h_manhattan_dist(center))
#    all_moves, total_nodes = a_star(mtx_node)
#    print("moves: {}\n total # of expanded nodes: {}".format(all_moves,total_nodes))
#    print("max num nodes in heap: ", global_max_q_len)
    
    #resets numNodes count in prep for next puzzle
    #global global_numNodes
#    global_numNodes = 0
#    global_max_q_len = 0
#    mtx_node = puzl_node(one_away, 0, calc_h_manhattan_dist(one_away))
#    all_moves, total_nodes = a_star(mtx_node)
#    print("moves: {}\n total # of expanded nodes: {}".format(all_moves, total_nodes))
#    print("max num nodes in heap: ", global_max_q_len)
#    print("             <<<<<<<<<<<<<    end")

#    global_numNodes = 0
#    global_max_q_len = 0
#    mtx_node = puzl_node(sample_sol, 0, calc_h_manhattan_dist(sample_sol))
#    all_moves, total_nodes = a_star(mtx_node)
#    print("moves: {}\n total # of expanded nodes: {}".format(all_moves, total_nodes))
#    print("max num nodes in heap: ", global_max_q_len)
#    print("             <<<<<<<<<<<<<    end")

    global_numNodes = 0
    global_max_q_len = 0
    mtx_node = puzl_node(sample_sol, 0, calc_h_manhattan_dist(sample_sol))
    all_moves, total_nodes = a_star(mtx_node)
    print("moves: {}\n total # of expanded nodes: {}".format(all_moves, total_nodes))
    print("max num nodes in heap: ", global_max_q_len)
    print("             <<<<<<<<<<<<<    end")
    


    return

#          00  01  02
#          10  11  12
#3 moves:RDR
sample_sol = [[1, 2, 3],
            [0, 4, 6],
            [7, 5, 8]]
#          20  21  22

#2 moves DR
sample_solution = [[1, 2, 3],
                [4, 0, 6],
                [7, 5, 8]]
main()