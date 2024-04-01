class GameState:
    def __init__(self, heaps):
        self.heaps = heaps

    def is_terminal(self):
        return all(heap == 0 for heap in self.heaps)

    def possible_moves(self):
        moves = []
        for i, heap in enumerate(self.heaps):
            for stones_removed in range(1, heap + 1):
                moves.append((i, stones_removed))
        return moves

    def make_move(self, move):
        heap, stones_removed = move
        new_heaps = list(self.heaps)
        new_heaps[heap] -= stones_removed
        return GameState(new_heaps)
    
    def get_real_answer(self):
        xr = 0
        for x in self.heaps:
            xr ^= x
        if xr == 0:
            return -1 
        return 1 