import random
from Battlefield import *
from Log import log

class BasicStrategy(object):
    def __init__(self, data):
        self.board = Board(data)

    def update(self, data):
        self.board.update(data)

    def findBestMove(self, beneficial, target):
        for areas in self.board.areas:
            for move in beneficial:
                log(f"Checking for area of size {target}, found area of size {len(areas)}")
                if move in areas and len(areas) >= target:
                    return move
                log (f"move: {move.x},{move.y} not accepted")
        for areas in self.board.areas:
            for move in beneficial:
                turns, newsize = self.board.turns_to_open(move)
                log(f"Checking for area of size {target}, found area of size {newsize} after {turns} turns")
                if newsize >= target and len(areas) > turns:
                    return move
        return None

    def basic_move(self):
        moves = self.board.possible_moves()
        moves_no_death = self.board.possible_moves_no_death()
        log(f"Possible Moves: {[self.board.my_snake.head.direction(x) for x in moves]}")
        log(f"Possible Moves No Death: {[self.board.my_snake.head.direction(x) for x in moves_no_death]}")

        head = self.board.my_snake.head
        head_up = head.up()
        head_down = head.down()
        head_left = head.left()
        head_right = head.right()

        if not moves:
            return UP
        closestFood = self.board.closest_food()
        log(f"Closest food: ({closestFood.x},{closestFood.y})")

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
                log(f"Beneficial Safe Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                move_to_take = self.findBestMove(beneficial, self.board.my_snake.length)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
            if self.board.my_snake.health >= (self.board.height + self.board.width):
                log(f"Nothing beneficial and not starving")
                move_to_take = self.findBestMove(moves_no_death, self.board.my_snake.length)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
        # moves is not empty
        log("Making a risky move")
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
            log(f"Beneficial Risky Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
            move_to_take = self.findBestMove(beneficial, self.board.my_snake.length)
            if move_to_take != None:
                return self.board.my_snake.head.direction(move_to_take)
        move_to_take = self.findBestMove(moves, self.board.my_snake.length)
        if move_to_take != None:
            return self.board.my_snake.head.direction(move_to_take)
        return self.board.my_snake.head.direction(random.choice(moves))