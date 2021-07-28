from operator import itemgetter
import copy


def create_goal_dictionary(goal_state):
    # Makes Dictionary Of Goal State Values and their location in 2d Matrix
    # Format {value at goal_state[0][0]:(0,0),goal_state[0][1]:(0,1),etc,etc}
    goal_dict = {}
    for i, row in enumerate(goal_state):
        for j, item in enumerate(row):
            goal_dict[item] = (i, j)

    return goal_dict


def calc_Manhatten(current_state, goal_dict):
    # Calculate Manhatten Distance Between Current State and Goal State
    # Sums all individuals Sums of  Difference Of x,y location of current state piece and goal state piece
    dist = 0
    for i, row in enumerate(current_state):
        for j, piece in enumerate(row):
            goal_piece_loc = goal_dict[piece]
            dist += abs(goal_piece_loc[0] - i) + abs(goal_piece_loc[1] - j)
    return dist


def get_possible_states(current_state):
    # Finds all possible states to move from current state
    possible_states = []

    # Location of movable empty piece
    emPieceLoc = []
    for i, row in enumerate(current_state):
        for j, item in enumerate(row):
            if item == 0:
                emPieceLoc = i, j
                break
        if emPieceLoc:
            break

    # Possible Moves For Empty Piece in 1 Move
    possible_moves_increments = [
        [-1, 0], [1, 0],
        [0, 1], [0, -1]
    ]
    # add possible increments to calculate possible states
    for increment in possible_moves_increments:
        possibleMove = [emPieceLoc[0] + increment[0], emPieceLoc[1] + increment[1]]

        # checks if new move lies inside puzzle
        if possibleMove[0] in [0, 1, 2] and possibleMove[1] in [0, 1, 2]:
            # Move Empty Piece according to possibleMove
            moved = copy.deepcopy(current_state)
            moved[emPieceLoc[0]][emPieceLoc[1]] = moved[possibleMove[0]][possibleMove[1]]
            moved[possibleMove[0]][possibleMove[1]] = 0
            possible_states.append(moved)

    return possible_states


def best_first_search(source, target):
    open = []  # The Opened Queue Storing Possible Moves.Moves Format (previous_state,current_state,Manhatten Distance Req For Move)
    closed = []  # The CLosed Queue Storing Visited Moves.Moves Format(current_state)
    MoveN = 0  # For counting move number

    goal_dict = create_goal_Dictionary(goal_state)
    open.append((source, 0))  # Default starting point
    print("Goal Dictionary: ", goal_dict)

    # Loop Will Run Till Open Queue Gets Empty
    while open:
        open = sorted(open, key=itemgetter(1))  # Sorts all possible moves ascending based on Manhatten Distance
        lowDistMove = open.pop(0)  # Dequeues Move with least Manhatten Distance(Optimal Move)
        closed.append(lowDistMove[0])  # Optimal Move is Visited
        open = []  # Empties Other Queue After Selecting Optimal Move
        # Printing Current State and Move No
        print("\nMove : ", MoveN)
        MoveN += 1
        print('\n'.join(['\t'.join([str(cell) if cell != 0 else ' ' for cell in row]) for row in lowDistMove[0]]))

        # Check Goal
        if lowDistMove[0] == target:
            print("\nGoal Achieved")
            break

        # Loops Around All States From Current State
        for n in get_possible_states(lowDistMove[0]):
            # possibleMove Format is (previous_state,current_state,Manhatten Distance)
            possibleMove = (n, calc_Manhatten(n, goal_dict))
            # BFS Algo: Checks Open and Closed Queue For Possible current_state
            openCurrentStates = [t[0] for t in open]
            if not (possibleMove[0] in openCurrentStates or possibleMove[0] in closed):
                # Append to Open If Not Found in Open or Closed Queue
                open.append(possibleMove)


initial_state = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]
#Change Goal State Here
goal_state = [
    [3, 2, 0],
    [8, 1, 4],
    [7, 6, 5]
]

best_first_search(initial_state, goal_state)

