from board import Direction, Rotation, Action, Shape
from random import Random
import time


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class JunwoosPlayer(Player):
    def __init__(self, seed=None):
        pass


    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)

    
    def get_heights(self, board):
        heights = [0] * board.width
        for x, y in board.cells:
            heights[x] = max(heights[x], board.height - y)
        return heights

    def calculate_lines_above_holes(self, board, heights):
        total_lines = 0
        for x in range(board.width):
            hole_height = heights[x]
            for y in range(hole_height + 1, board.height):
                if (x, y) not in board.cells:
                    break  # Stop when an empty space is encountered
                total_lines += 1
        return total_lines

    
    def calculate_well_bonus(self, board):
        well_bonus = 0
        for x in range(board.width-8):
            well_depth = self.calculate_well_depth(board, x)
            well_bonus += well_depth

        return well_bonus

    def calculate_well_depth(self, board, x):
        # Calculate the depth of a well at column x
        well_depth = 0
        for y in range(board.height - 2, -1, -1):
            if (x, y) not in board.cells and (x - 1, y) in board.cells and (x + 1, y) in board.cells:
                well_depth += 1
            else:
                break

        return well_depth
        
    def lines_cleared(self):
        cells_diff = self.new_cells - self.old_cells
        if cells_diff == -2:
            return 50
        elif cells_diff == -12:
            return 100
        elif cells_diff == -22:
            return 400
        else:
            return 0
        
    def fourlines_cleared(self):
        cells_diff = self.new_cells - self.old_cells
        if cells_diff == -32:
            return 1
        else :
            return 0

    def score(self, board):
        weight_max_height= -7
        weight_hole_penalty= 600
        weight_num_cleared_lines= 0
        weight_fourlines_cleared = 0
        weight_above_holes = 18
        weight_bumpiness = 90
        weight_well_bonus = 15

        heights = self.get_heights(board)
        max_height = max(heights) * weight_max_height 

        score =+ max_height 

        well_bonus = self.calculate_well_bonus(board)
        score += well_bonus * weight_well_bonus

        fourlinebonus= self.fourlines_cleared()
        score += weight_fourlines_cleared * fourlinebonus

        num_holes =0 
        for x in range (board.width):
            for y in range(heights[x] -1,-1,-1):
                if (x,board.height -y -1) not in board.cells:
                    num_holes += 1
        score -= weight_hole_penalty * num_holes

        num_cleared_lines = self.lines_cleared()
        score += num_cleared_lines * weight_num_cleared_lines 

        lines_above_holes = self.calculate_lines_above_holes(board, heights)
        score += lines_above_holes * weight_above_holes

        bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(board.width-1))
        score -= bumpiness * weight_bumpiness

        return score


    
    def move_to_target(self, board, target_x, target_r):
        moves = []
        has_landed = False
        while not has_landed and target_r != 0:
            if target_r == 3:
                moves.append(Rotation.Anticlockwise)
                has_landed = board.rotate(Rotation.Anticlockwise)
                break
            moves.append(Rotation.Clockwise)
            has_landed = board.rotate(Rotation.Clockwise)
            target_r -= 1
        
        while not has_landed and target_x > board.falling.left  :
            moves.append(Direction.Right)
            has_landed = board.move(Direction.Right)
        while not has_landed and target_x < board.falling.left  :
            moves.append(Direction.Left)
            has_landed = board.move(Direction.Left)
        
        if not has_landed:
            moves.append(Direction.Drop)
            board.move(Direction.Drop)
        
        return moves


    def choose_action(self, board):
        possibilities = []
        for r in range(4):
            for x in range(board.width - (board.falling.right - board.falling.left)):
                b = board.clone()
                self.old_cells = len(b.cells)
                moves = self.move_to_target(b, x, r)
                for r2 in range(4):
                    for x2 in range(board.width - (board.falling.right - board.falling.left)):
                        c = b.clone()
                        moves += self.move_to_target(c, x2, r2)
                        self.new_cells = len(c.cells)
                        possibilities.append((self.score(c), moves))
        _, moves = max(possibilities, key=lambda x: x[0])
        return moves

        

SelectedPlayer = JunwoosPlayer
