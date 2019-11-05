import heapq as minheap_q #ref: inspired from Lorem Ipsum project sample

#general srch alg: (from project briefing)
#arg1: problem(init state)
#arg2: queueing-function
#function srch_1,2or3(arg1, arg2):
#nodes = make node init state and enqueue node init state 
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

#value: the key's index position w.r.t matrices   
goal_dict = {1:[0,0],
            2:[0,1],
            3:[0,2],
            4:[1,0],
            5:[1,1],
            6:[1,2],
            7:[2,0],
            8:[2,1]}

#h(n) = heuristic that /underestimates/
#   the sum of /each/ tile's_distance_to_desired_pos

def calc_h_manhattan_dist(puzl_list):
    sum = 0
    for y in range(len(puzl_list)): #rowNum 0,1,2
        for x in range(len(puzl_list[0])):
            if puzl_list[y][x] != 0: #0 has no dict
                yIndx_of_goal, xIndx_of_goal = goal_dict.get(puzl_list[y][x])
                #formula reference @ line21,22
                sum += abs(yIndx_of_goal - y) + abs(xIndx_of_goal - x)
    return sum


def main():
    h_md_sample_sol = calc_h_manhattan_dist(sample_sol)
    print("solution = 3: ", h_md_sample_sol)

    h_md_trivial = calc_h_manhattan_dist(trivial)
    print("solution = 0: ", h_md_trivial)

    h_md_oneAway = calc_h_manhattan_dist(one_away)
    print("solution = 1: ", h_md_oneAway)

    h_md_mustTrace = calc_h_manhattan_dist(must_trace)
    print("solution = 2: ", h_md_mustTrace)

    return

main()
#create all possible matrices(except repeated states)