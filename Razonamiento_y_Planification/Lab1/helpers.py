import copy

class State:
    def __init__(self, table, pile):
        self.table = table
        self.pile = pile

    def __repr__(self):
        return f'State: Table {self.table}, Pile {self.pile}'

    def __eq__(self, other):
        if (self.table == other.table) and (self.pile == other.pile):
            return True
        else:
            return False

    def put(self, piece):
        # Put piece from table to pile
        if piece in self.table:
            n = copy.deepcopy(self)
            n.pile.append(piece)
            n.table.remove(piece)
            return n
        else:
            None

    def get(self):
        # Remove a piece from the pile and put it on the table
        try:
            n = copy.deepcopy(self)
            piece = n.pile.pop()
            n.table.append(piece)
            return n
        except IndexError:
            return None

class Node:
    nnodes = 0
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.nodeid = Node.nnodes
        Node.nnodes+=1

        # Used by heuristics to evaluate node
        self.rateing = 0

    def put(self, piece):
        ns = self.state.put(piece)
        if ns:
            return Node(self, ns)
        else:
            return None
    
    def get(self):
        ns = self.state.get()
        if ns:
            return Node(self, ns)
        else:
            return None

    def __repr__(self):        
        if self.parent:
            return f'N {self.nodeid}, R {self.rateing} :[ P {self.parent.nodeid}, {self.state}]'
        else:
            return f'N {self.nodeid}, R {self.rateing} :[ P None, {self.state}]'