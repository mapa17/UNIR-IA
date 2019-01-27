from helpers import Node, State
from copy import copy
import sys

# this is a pointer to the module object instance itself.
this = sys.modules[__name__]
this.expansion_count = 0

def bfs_search(current_node, node_list, final_state, state_space):
    if current_node.state == final_state:
        return current_node

    successors = expand(current_node, state_space)

    # Avoid simple loops
    if current_node.parent:
        # Dont add successors if they have the same state as the parent
        keep = list(filter(lambda s: s.state != current_node.parent.state, successors))
        successors = keep

    # Append to stack
    node_list += successors

    # Use breadth search
    try:
        next_node = node_list.pop(0)
    except IndexError:
        # No solution found!
        return None

    return bfs_search(next_node, node_list, final_state, state_space)


def aStar_search(current_node, node_list, final_state, state_space):
    if current_node.state == final_state:
        return current_node

    successors = expand(current_node, state_space)

    # Avoid simple loops
    if current_node.parent:
        # Dont add successors if they have the same state as the parent
        keep = list(filter(lambda s: s.state != current_node.parent.state, successors))
        successors = keep

    # Use a heuristic to evaluate the quality of each node
    rate_nodes(current_node, successors, final_state)

    # Append to stack
    node_list += successors
    node_list = sorted(node_list, key=lambda node: node.rateing, reverse=False)

    # Use breadth search
    try:
        next_node = node_list.pop(0)
    except IndexError:
        # No solution found!
        return None

    return aStar_search(next_node, node_list, final_state, state_space)


def rate_nodes(current_node, simple_node_list, final_state):
    # Rate the state of a note compared to the final state
    # Give a positive score for each correct piece on the pile and table
    # in addition to giving a negative score for pieces in the wrong order 
    # on the pile or if there are some on the table and the solution has none.

    for n in simple_node_list:
        rateing = 0
        table = copy(n.state.table)
        pile = copy(n.state.pile)

        # Compare the table pieces
        for fp in final_state.table:
            try:
                if fp == table.pop(0):
                    rateing -= 1
                    pass
                else:
                    rateing += 1
            except IndexError:
                rateing += 1
        rateing += len(table)

        # Compare the pile pieces
        for fp in final_state.pile:
            try:
                if fp == pile.pop(0):
                    rateing -= 2
                    pass
                else:
                    rateing += 2
            except IndexError:
                rateing += 1
        rateing += len(pile)

        rateing += max(current_node.rateing, 0)

        # Assign the rating
        n.rateing = rateing



def expand(node, state_space):
    # Track the number of expansions
    this.expansion_count += 1

    # Expand a node with all possible actions for its current state
    successors = []

    # Remove from pile
    nnode = node.get()
    if nnode:
        successors.append(nnode)

    for piece in state_space:
        nnode = node.put(piece)
        if nnode:
            successors.append(nnode)

    return successors    

