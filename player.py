from board import Direction, Rotation, Action
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


    def score(self, board):
        heights = self.get_heights(board)
        max_height = max(heights)

        score =-max_height

        #num_holes = sum(max_height - h for h in heights)
        #score -= num_holes

        num_cleared_lines = board.clean()
        score += num_cleared_lines * 100

        #bumpiness = sum(abs(heights[i] - heights[i + 1]) for i in range(board.width - 1))
        #score -= bumpiness

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
        
        while not has_landed and target_x > board.falling.left:
            moves.append(Direction.Right)
            has_landed = board.move(Direction.Right)
        while not has_landed and target_x < board.falling.left:
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
                moves = self.move_to_target(b, x, r)
                possibilities.append((self.score(b), moves))
        _, moves = max(possibilities, key=lambda x: x[0])
        return moves

        

SelectedPlayer = JunwoosPlayer
