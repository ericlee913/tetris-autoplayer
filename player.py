from board import Direction, Rotation
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
                    break  
                total_lines += 1
        return total_lines
        
    def lines_cleared(self):
        cells_diff = self.new_cells - self.old_cells
        if cells_diff == -2:
            return -975
        elif cells_diff == -12:
            return -650
        elif cells_diff == -22:
            return -350
        else:
            return 0
        
    def fourlines_cleared(self):
        cells_diff = self.new_cells - self.old_cells
        if cells_diff == -32:
            return 1
        else :
            return 0

    def score(self, board):
        weight_max_height= -20
        weight_hole_penalty= 1700
        weight_num_cleared_lines= 1
        weight_fourlines_cleared = 2300
        weight_above_holes = 22
        weight_bumpiness = 230

        heights = self.get_heights(board)
        max_height = max(heights)  
        height_penalty= max_height * weight_max_height

        score =+ height_penalty 

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
        for rotation in range(4):
            for x in range(board.width - (board.falling.right - board.falling.left)):
                clone1 = board.clone()
                self.old_cells = len(clone1.cells)
                moves = self.move_to_target(clone1, x, rotation)
                for rotation2 in range(4):
                    for x2 in range(board.width - (board.falling.right - board.falling.left)):
                        clone2 = clone1.clone()
                        moves += self.move_to_target(clone2, x2, rotation2)
                        self.new_cells = len(clone2.cells)
                        possibilities.append((self.score(clone2), moves))
        _, moves = max(possibilities, key=lambda x: x[0])
        return moves

        

SelectedPlayer = JunwoosPlayer
