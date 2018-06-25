import copy
import queue



class Kuromasu:
    instances = 0
    steps = 0

    def __init__(self, board, parent=None):
        self.parent = parent
        self.board = copy.deepcopy(board)
        Kuromasu.instances += 1

    def __str__(self):
        out = '\n'.join([' '.join([cell for cell in row if cell != 'x']) for row in self.board if row.count('x') <= 2])
        return out

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.board == other.board

    def __hash__(self):
        """Shift-Add-XOR hash function."""
        h = 0
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                h ^= (h << 5) + (h >> 2) + ord(self.board[r][c])
        return h

    def __lt__(self, other):
        self_priority = self.f()
        other_priority = other.f()
        return self_priority < other_priority

    @staticmethod
    def reset():
        Kuromasu.instances = 0
        Kuromasu.steps = 0

    def create_padding(self):
        """Create padding for easy bounds checking.""" 
        for row in self.board:
            row.insert(0, 'x')
            row.append('x')
        self.board.insert(0, ['x' for i in range(len(self.board[0]))])
        self.board.append(['x' for i in range(len(self.board[0]))])


    def is_solved(self):
        """Check if the board is in a correct state within the game rules."""  
        return (self.check_white_cells_visible_from_numbers() 
                and self.check_all_white_cells_accessible()
                and self.check_black_cells_separate())


    def check_white_cells_visible_from_numbers(self):
        number_cells = self.get_number_cells()

        for position in number_cells:
            row, col = position
            if int(self.board[row][col]) != self.count_white_cells_visible_from_number(position):
                return False
        return True

    def get_number_cells(self):
        number_cells = [(r, c) for r in range(1, len(self.board)) for c in range(1, len(self.board)) if self.board[r][c].isnumeric() and self.board[r][c] != '0']
        return number_cells

    def count_white_cells_visible_from_number(self, position):
        row, col = position
        # numbered cell is always visible
        visible = 1
        # north
        for i in range(row - 1, 0, -1):
            if self.board[i][col].isnumeric():
                visible += 1
            else:
                break
        # south
        for i in range(row + 1, len(self.board)):
            if self.board[i][col].isnumeric():
                visible += 1
            else:
                break
        # west
        for i in range(col - 1, 0, -1):
            if self.board[row][i].isnumeric():
                visible += 1
            else:
                break
        # east
        for i in range(col + 1, len(self.board)):
            if self.board[row][i].isnumeric():
                visible += 1
            else:
                break
        return visible

    
    def check_all_white_cells_accessible(self):
        """
        Traverse all connected white cells, check with total white cells.
        WHITE_CELLS = ALL_CELLS - BLACK_CELLS.
        """ 
        connected = 0
        visited = []
        A = []
        A.append(self.get_first_white_cell())
        while A:
            cell = A.pop()
            if cell not in visited:
                visited += [cell]
                neighbors = self.get_neighboring_white_cells(cell)
                A += neighbors
                connected += 1
        return connected == (self.count_cells_total() - self.count_black_cells_total())

    def get_first_white_cell(self):
        positions = [(r, c) for r in range(1, len(self.board)) for c in range(1, len(self.board)) if self.board[r][c].isnumeric()]
        return positions[0]

    def get_neighboring_white_cells(self, position):
        white_cells = []
        row, col = position
        for (r, c) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.board[row+r][col+c].isnumeric():
                white_cells.append((row+r, col+c))
        return white_cells

    def count_cells_total(self):
        return (len(self.board) - 2) * (len(self.board) - 2)

    def count_black_cells_total(self):
        black_cells_count = [(r, c) for r in range(1, len(self.board)) for c in range(1, len(self.board)) if self.board[r][c] == '#']
        return len(black_cells_count)


    def check_black_cells_separate(self):
        black_cells = self.get_black_cells()
        for position in black_cells:
            row, col = position
            for (r, c) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if self.board[row+r][col+c] == '#':
                    return False
        return True

    def get_black_cells(self):
        black_cells = [(r, c) for r in range(len(self.board)) for c in range(len(self.board)) if self.board[r][c] == '#']
        return black_cells 


    def get_new_states(self):
        """Generate new board states in a nested loop to exhaust every possibility."""
        states = []
        row, col = self.get_first_white_cell()
        for r in range(row, len(self.board)):
            for c in range(col, len(self.board)):
                if self.board[r][c] == '0':
                    self.board[r][c] = '#'
                    states += [Kuromasu(board, self)]
                    # perserve previous state
                    self.board[r][c] = '0'
        return states

    def h(self):
        correct_number_cells = 0
        number_cells = self.get_number_cells()
        for position in number_cells:
            row, col = position
            if int(self.board[row][col]) == self.count_white_cells_visible_from_number((row, col)):
                correct_number_cells += 1
        return len(number_cells) - correct_number_cells

    def f(self):
        """
        Objective function f(n).
        g(x) corresponds to the amount of steps taken,
        h(x) corresponds to the amount of correct number cells.
        """ 
        return Kuromasu.steps + self.h()


    @staticmethod
    def solve_dfs(board):
        start_state = Kuromasu(board)
        start_state.create_padding()
        if start_state.is_solved():
            return start_state, Kuromasu.steps, Kuromasu.instances

        A = queue.LifoQueue()
        visited = set()
        A.put(start_state)
        visited.add(start_state)
        while not A.empty():
            state = A.get()
            if state.is_solved():
                return state.__str__(), Kuromasu.steps, Kuromasu.instances
            for new_state in state.get_new_states():
                if new_state not in visited:
                    visited.add(new_state)
                    A.put(new_state)
            Kuromasu.steps += 1
        return 'UNSOLVABLE', Kuromasu.steps, Kuromasu.instances
            

    @staticmethod
    def solve_a_star(board):
        start_state = Kuromasu(board)
        start_state.create_padding()
        if start_state.is_solved():
            return start_state, Kuromasu.steps, Kuromasu.instances
        
        A = queue.PriorityQueue()
        visited = set()
        A.put(start_state)
        visited.add(start_state)
        while not A.empty():
            state = A.get()
            if state.is_solved():
                return state.__str__(), Kuromasu.steps, Kuromasu.instances
            for new_state in state.get_new_states():
                if new_state not in visited:
                    visited.add(new_state)
                    A.put(new_state)
            Kuromasu.steps += 1
        return 'UNSOLVABLE', Kuromasu.steps, Kuromasu.instances


#def main():
#    BOARD = [
#        ['4', '0', '0'],
#        ['0', '0', '0'],
#        ['0', '0', '4'],
#    ]
#
#    print("DFS:")
#    result, steps, instances = Kuromasu.solve_dfs(copy.deepcopy(BOARD))
#    print(result)
#    print("step count: ", steps)
#    print("instances created: ", instances)
#    print()
#
#    Kuromasu.reset()
#    print("A*:")
#    result, steps, instances = Kuromasu.solve_a_star(copy.deepcopy(BOARD))
#    print(result)
#    print("step count: ", steps)
#    print("instances created: ", instances)
#    print() 
#
#if __name__ == "__main__":
#    main()