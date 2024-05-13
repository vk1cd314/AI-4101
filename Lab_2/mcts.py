from abc import ABC, abstractmethod
from collections import defaultdict
import math

class MCTS:
    def __init__(self, exploration_weight=math.sqrt(2)):
        self.Q = defaultdict(int) 
        self.N = defaultdict(int) 
        self.children = dict() 
        self.exploration_weight = exploration_weight
        self.nodes_visited = 0

    def choose(self, node):
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf") 
            return self.Q[n] / self.N[n] 

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        self.nodes_visited = 0
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        path = []
        while True:
            path.append(node)
            self.nodes_visited += 1
            if node not in self.children or not self.children[node]:
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                self.nodes_visited += 1
                return path
            node = self._uct_select(node) 

    def _expand(self, node):
        if node in self.children:
            return 
        self.children[node] = node.find_children()

    def _simulate(self, node):
        invert_reward = True
        while True:
            self.nodes_visited += 1
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.find_random_child()
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward 

    def _uct_select(self, node):
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)

    def get_nodes_visited(self):
        return self.nodes_visited

class Node(ABC):
    @abstractmethod
    def find_children(self):
        return set()

    @abstractmethod
    def find_random_child(self):
        return None

    @abstractmethod
    def is_terminal(self):
        return True

    @abstractmethod
    def reward(self):
        return 0

    @abstractmethod
    def __hash__(self):
        return 123456789

    @abstractmethod
    def __eq__(node1, node2):
        return True