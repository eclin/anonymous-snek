import random
from Battlefield import *

class BasicStrategy(object):
    def __init__(self, data):
        self.board = Board(data)

    def update(self, data):
        self.board.update(data)

    def basic_move(self):
        moves = self.board.possible_moves()
        moves_no_death = self.board.possible_moves_no_death()
        print(f"Possible Moves: {moves}")
        if not moves:
            return "up"
        closestFood = self.board.closest_food()
        if not moves_no_death:
            ret = None
            if ("right" in moves_no_death) and (self.board.my_snake.head.x < closestFood.x):
                ret = "right"
            elif ("left" in moves_no_death) and (self.board.my_snake.head.x > closestFood.x):
                ret = "left"
            else:
                if ("down" in moves_no_death) and (self.board.my_snake.head.y < closestFood.y):
                    ret = "down"
                elif ("up" in moves_no_death) and (self.board.my_snake.head.y > closestFood.y):
                    ret = "up"
            # if health is greater than threshold then dont take a riskier move
            if ret != None:
                return ret
            if self.board.my_snake.health >= 2 * (self.board.height + self.board.width):
                return random.choice(moves_no_death) 
        # moves is not empty
        if ("right" in moves) and (self.board.my_snake.head.x < closestFood.x):
            return "right"
        elif ("left" in moves) and (self.board.my_snake.head.x > closestFood.x):
            return "left"
        else:
            if ("down" in moves) and (self.board.my_snake.head.y < closestFood.y):
                return "down"
            elif ("up" in moves) and (self.board.my_snake.head.y > closestFood.y):
                return "up"
        # TODO: can potentially mark certain moves as less dangerous and take the least dangerous move
        return random.choice(moves)         

