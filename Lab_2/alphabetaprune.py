import math

class AlphaBetaPruningAgent:
    def __init__(self):
        self.states_visited = 0
        
    def alphabetapruning(self, state, alpha, beta, maximizing_player):
        self.states_visited += 1
        if state.is_terminal():
            return -1 if maximizing_player else 1

        if maximizing_player:
            max_eval = -math.inf
            for move in state.possible_moves():
                eval = self.alphabetapruning(state.make_move(move), alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for move in state.possible_moves():
                eval = self.alphabetapruning(state.make_move(move), alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_seq_moves(self, state):
        self.states_visited = 0 
        res = []
        mov = 0
        while not state.is_terminal():
            if mov:
                best_eval = math.inf
                best_move = None
                for move in state.possible_moves():
                    eval = self.alphabetapruning(state.make_move(move), -math.inf, math.inf, True)
                    if eval < best_eval:
                        best_eval = eval
                        best_move = move
                res.append(best_move)
                state = state.make_move(best_move)
            else:
                best_eval = -math.inf
                best_move = None
                for move in state.possible_moves():
                    eval = self.alphabetapruning(state.make_move(move), -math.inf, math.inf, False)
                    if eval > best_eval:
                        best_eval = eval
                        best_move = move
                res.append(best_move)
                state = state.make_move(best_move)
            mov ^= 1
        return res
    
    def get_states_visited(self):
        return self.states_visited