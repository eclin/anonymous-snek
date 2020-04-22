import random
from Battlefield import *

class BasicStrategy(object):
    def __init__(self, data):
        self.board = Board(data)

    def update(self, data):
        self.board.update(data)

    def findBestMove(self, beneficial):
        for areas in self.board.areas:
            for move in beneficial:
                if move in areas:
                    return move, len(areas)

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

        beneficial = []

        if moves_no_death:
            if (head_right in moves_no_death) and (self.board.my_snake.head.x < closestFood.x):
                beneficial.append(head_right)
            elif (head_left in moves_no_death) and (self.board.my_snake.head.x > closestFood.x):
                beneficial.append(head_left)
            if (head_down in moves_no_death) and (self.board.my_snake.head.y < closestFood.y):
                beneficial.append(head_down)
            elif (head_up in moves_no_death) and (self.board.my_snake.head.y > closestFood.y):
                    beneficial.append(head_up)
            # if health is greater than threshold then dont take a riskier move
            if beneficial:
                print(f"Beneficial Safe Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                move_to_take, area = self.findBestMove(beneficial)
                print(f"Area of potential new beneficial safe area: {area}")
                if area > self.board.my_snake.length or self.board.my_snake.health < 2 * (self.board.height + self.board.width):
                    return self.board.my_snake.head.direction(move_to_take)
            if self.board.my_snake.health >= 2 * (self.board.height + self.board.width):
                print(f"Nothing beneficial and not starving")
                move_to_take, area = self.findBestMove(moves_no_death)
                print(f"Area of potential new safe area: {area}")
                return self.board.my_snake.head.direction(move_to_take)
        # moves is not empty
        print("Making a risky move")
        beneficial.clear()
        if (head_right in moves) and (self.board.my_snake.head.x < closestFood.x):
            beneficial.append(head_right)
        elif (head_left in moves) and (self.board.my_snake.head.x > closestFood.x):
            beneficial.append(head_left)
        if (head_down in moves) and (self.board.my_snake.head.y < closestFood.y):
            beneficial.append(head_down)
        elif (head_up in moves) and (self.board.my_snake.head.y > closestFood.y):
            beneficial.append(head_up)
        # TODO: can potentially mark certain moves as less dangerous and take the least dangerous move
        if beneficial:
            print(f"Beneficial Risky Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
            move_to_take, area = self.findBestMove(beneficial)
            print(f"Area of potential new risky area: {area}")
            return self.board.my_snake.head.direction(move_to_take)
        else:
            move_to_take, area = self.findBestMove(moves)
            print(f"Area of potential new risky death area: {area}")
            return self.board.my_snake.head.direction(move_to_take)
