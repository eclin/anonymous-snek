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
        print(f"Possible Moves: {[self.board.my_snake.head.direction(x) for x in moves]}")
        print(f"Possible Moves No Death: {[self.board.my_snake.head.direction(x) for x in moves_no_death]}")

        head = self.board.my_snake.head
        head_up = head.up()
        head_down = head.down()
        head_left = head.left()
        head_right = head.right()

        if not moves:
            return UP
        closestFood = self.board.closest_food()
        print(f"Closest food: ({closestFood.x},{closestFood.y})")

        if moves_no_death:
            ret = None
            if (head_right in moves_no_death) and (self.board.my_snake.head.x < closestFood.x):
                ret = RIGHT
            elif (head_left in moves_no_death) and (self.board.my_snake.head.x > closestFood.x):
                ret = LEFT
            else:
                if (head_down in moves_no_death) and (self.board.my_snake.head.y < closestFood.y):
                    ret = DOWN
                elif (head_up in moves_no_death) and (self.board.my_snake.head.y > closestFood.y):
                    ret = UP
            # if health is greater than threshold then dont take a riskier move
            print(f"moves_no_death ret = {ret}")
            if ret != None:
                return ret
            if self.board.my_snake.health >= 2 * (self.board.height + self.board.width):
                return self.board.my_snake.head.direction(random.choice(moves_no_death))
        # moves is not empty
        print("Making a risky move")
        if (head_right in moves) and (self.board.my_snake.head.x < closestFood.x):
            return RIGHT
        elif (head_left in moves) and (self.board.my_snake.head.x > closestFood.x):
            return LEFT
        else:
            if (head_down in moves) and (self.board.my_snake.head.y < closestFood.y):
                return DOWN
            elif (head_up in moves) and (self.board.my_snake.head.y > closestFood.y):
                return UP
        # TODO: can potentially mark certain moves as less dangerous and take the least dangerous move
        return self.board.my_snake.head.direction(random.choice(moves))
