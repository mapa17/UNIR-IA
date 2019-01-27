# Lab 1
# Participants: Gonzalo Molina, David Pineiro, Oscar Piqueras, Manuel Pasieka, Samuel Eduardo
from helpers import State, Node
from algorithms import bfs_search, aStar_search
import algorithms
from pudb import set_trace as st

state_space = [1, 2, 3, 4, 5, 6]
initial_state = State([1, 6, 3], [2, 4, 5])
final_state = State([], [1, 2, 3, 4, 5, 6])

#state_space = [1, 2, 3, 4, 5]
#initial_state = State([1, 3], [2, 4, 5])
#final_state = State([], [1, 2, 3, 4, 5])
#final_state = State([5], [1, 2, 3, 4])

#state_space = [1, 2, 3, 4]
#initial_state = State([2, 3], [1])
#initial_state = State([1, 4], [3, 2])
#final_state = State([], [1, 2, 3, 4])

#state_space = [1, 2, 3]
#initial_state = State([2, 3], [1])
#initial_state = State([1, 3], [2])
#final_state = State([], [1, 2, 3])

if __name__ == '__main__':

    root = Node(None, initial_state)

    #solution = bfs_search(root, [], final_state, state_space)
    
    solution = aStar_search(root, [], final_state, state_space)
    

    path = [solution]
    while solution.parent:
        solution = solution.parent
        path.append(solution)
    
    print(f'Solution Path\n{path[::-1]}')
    print(f'It took {algorithms.expansion_count} expansions (equal to depth)')
