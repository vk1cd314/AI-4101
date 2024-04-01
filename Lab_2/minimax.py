import math

class MinimaxAgent:
    def minimax(self, state, maximizing_player):
        if state.is_terminal():
            return -1 if maximizing_player else 1

        if maximizing_player:
            max_eval = -math.inf
            for move in state.possible_moves():
                eval = self.minimax(state.make_move(move), False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in state.possible_moves():
                eval = self.minimax(state.make_move(move), True)
                min_eval = min(min_eval, eval)
            return min_eval

    def best_seq_moves(self, state):
        res = []
        mov = 0
        while not state.is_terminal():
            if mov:
                best_eval = math.inf
                best_move = None
                for move in state.possible_moves():
                    eval = self.minimax(state.make_move(move), True)
                    if eval < best_eval:
                        best_eval = eval
                        best_move = move
                res.append(best_move)
                state = state.make_move(best_move)
            else:
                best_eval = -math.inf
                best_move = None
                for move in state.possible_moves():
                    eval = self.minimax(state.make_move(move), False)
                    if eval > best_eval:
                        best_eval = eval
                        best_move = move
                res.append(best_move)
                state = state.make_move(best_move)
            mov ^= 1
        return res