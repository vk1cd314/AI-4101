from collections import namedtuple
from mcts import MCTS, Node
from random import choice, randint
from copy import deepcopy

class NimPiles(Node):
    def __init__(self, heaps):
        self.heaps = heaps

    def find_children(self):
        res = set()
        for i, heap in enumerate(self.heaps):
            for take in range(1, heap + 1):
                new_heap = deepcopy(self.heaps)
                new_heap[i] -= take
                res.add(NimPiles(new_heap))
        return res

    def find_random_child(self):
        if len(self.heaps) == 1:
            index = 0
        else:
            opts = []
            for i, heap in enumerate(self.heaps):
                if heap != 0:
                    opts.append(i)
            index = choice(opts)
        
        if self.heaps[index] == 1:
            take = 1
        else:
            take = randint(1, self.heaps[index])
            
        new_heap = deepcopy(self.heaps)
        new_heap[index] -= take
        return NimPiles(new_heap)

    def is_terminal(self):
        return sum(self.heaps) == 0

    def reward(self):
        return 0 if self.is_terminal() else 1
    
    def __hash__(self):
        return hash(tuple(self.heaps))

    def __eq__(node1, node2):
        return node1.heaps == node2.heaps