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
# abs(xIndx - xIndx_of_goal) + abs(yIndx - yIndx_of_goal) 
# above formula's reference: #ref: https://stackoverflow.com/questions/39759721/calculating-the-manhattan-distance-in-the-eight-puzzle
# |2-2| + |2-1| = 1
must_trace = [[1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]]
            #sol = 2

#sample project: num nodes expanded: 13
            #   :max queue size: 8

#          00  01  02
#          10  11  12
sample_sol = [[1, 2, 3],
            [0, 4, 6],
            [7, 5, 8]]
#          20  21  22
#5: |2-1| + |1-1| = 1
#4: |1-1| + |1-0| = 1
#manhattan: 4: 1 away
#           5: 1
#           8: 1
# h(n) = total = 3 
center = [[1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]]

#value: the key's index position w.r.t matrices   
goal_dict = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2],
            7:[2,0], 8:[2,1]}

#a list of tuples of moves the 0 can do in a matrix
#U: 11-> 01
#D: 01-> 11
#L: 11-> 10
#R: 11-> 12
add_move = [('U', (-1,0)), 
            ('D', (1,0)),
            ('L', (0,-1)),
            ('R', (0, 1))]

global_heuristic = ""
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
#creating nodes class that rep puzl matrices and val = g + h
#how2use: insert g+h as arg to get total val
#purpose: creates a trace from root to goal node + respective cost vals
class puzl_node:
    def __init__(self, mtx, g_val=0, h_val=0, zero_pos=(2,2)):
        self.mtx = copy.deepcopy(mtx) #deep copies the mtx(list)
        self.g_val = g_val
        self.h_val = h_val
        self.f_val = self.g_val + self.h_val
        self.zero_pos = locate_zero_pos(self.mtx)
        #fixme: need parent? maybenot?
        self.parent = None
        self.nextNode = None
        
        #fixme: rm: points to list(matrix) where 0 moves up

        #self.nextNode_down = None #" " where 0 moves down

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
def possible_mtx_nodes(node):
    #fixme: change if to for
    
    print("within poss_mtx_node; printing orig mtx:")
    print_mtx(node.mtx)
    #tuple unpacking of the ordered list: add_move
    print("           >>>>>>>>>>>")
    for move, add_position in add_move:
        new_mtx = copy.deepcopy(node.mtx)
        print(node.zero_pos)
        #unpacking the addition of the tuples
        new_y_zero_pos = (node.zero_pos)[0] + add_position[0]
        new_x_zero_pos = (node.zero_pos)[1] + add_position[1]
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
                                        (new_y_zero_pos, new_x_zero_pos))

        print("printing node's new mtx:   ")
        print_nodes_mtx(new_mtx_node)
        print("                  <<<<<<<<<<<<<<<<<<<<")
    return

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
                #formula reference @ line21,22
                sum += abs(yIndx_of_goal - y) + abs(xIndx_of_goal - x)
    return sum


#TODO: implement formula for g
#fixme? is this what I want? function: the curr cost of curr node path
#
#fixme? should up/down moves cost 2 while L/R cost 1?

#first impl: each move = 1
#arg = node
# returns node's g_val
#fixme: might not need this. could just incr directly in the node
def calc_g(node):
    node.g_val += 1 #incr g_val by one after a move is made
    return
 
#checks whether curr node is the goal state
#1.if heuristic == manhattan, goal == if h(n) == 0
# if heuristic == hamming, goal == if h(n) == 0
#2.if using uniform cost fcn: must check if each tile is in correct place
#arg: node.val which contains the matrix(list)
#todo: impl 2 and 3
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


#arg: init_node = a node from main()
def a_star(init_node):
    minheap = [] #init minheap
    #2nd arg: a tuple of f(n) and the deepcopied mtx
    #minheap: the lowest f_val is the root
    heapq.heappush(minheap, (init_node.f_val, init_node)) #fixme? make get_f_val?

    #while(bool_not_goal_state)
    #   1. assign parent variable=root node
    #   2.insert nodes of next states' possible moves (up,down,L,R)
    #       >first copy parent node, then make alteration
    #       >the minheap will auto move the lowest_val_node into root
    #   3.assign 
    #   4.pop the root node
    #       the non-root node with the lowest val gets moved to top of minheap
    #       check if root==goal state
    #       print root
    #       keep not_goal_state true
    #return to top of while(not_goal_state) loop and do all over again until not_goal_state==false
    
    return

#global variables:
global_heuristic = "manhattan"

def main():
#tests:
    #h_md_sample_sol = calc_h_manhattan_dist(sample_sol)
    #print("solution = 3: ", h_md_sample_sol)

    #h_md_trivial = calc_h_manhattan_dist(trivial)
#    print("solution = 0: ", h_md_trivial)
    ###trivial_mtx_node = puzl_node(trivial) #inserts trivial mtx into initial_state node
    ###trivial_mtx_node.h_val = calc_h_manhattan_dist(trivial)
    ###a_star(trivial_mtx_node)
    ###if goal_test()

 #   h_md_oneAway = calc_h_manhattan_dist(one_away)
  #  print("solution = 1: ", h_md_oneAway)

    #1st arg: mtx, 2nd arg: g, 3rd arg: h, 4th:zero_pos
    mtx_node = puzl_node(center, 0, calc_h_manhattan_dist(center))
    #print("goal test should be false at this point: ", goal_test(mtx_node)) 
    #print("testing matrix==trivial:", equal_trivial(trivial))
    #print(print_mtx(center))
    #print(locate_zero_pos(center))
    #print(mtx_node.zero_pos)
    print(" >>>>>>>    <<<<<<<")
    possible_mtx_nodes(mtx_node)


    ###a_star(mtx_node)
    ###if goal_test()

   # h_md_mustTrace = calc_h_manhattan_dist(must_trace)
    #print("solution = 2: ", h_md_mustTrace)

    return
#python3: don't need if__name
main()

#stick init state list into minheap
#expand depending on g+h