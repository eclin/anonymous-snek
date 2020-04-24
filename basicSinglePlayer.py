import random
from Battlefield import *
from Log import log

class BasicStrategy(object):
    def __init__(self, data):
        self.board = Board(data)

    def update(self, data):
        self.board.update(data)

    def findBestMove(self, beneficial, target):
        # since the areas are sorted in decreasing size, the best move will be the move that appears
        # in the earliest area since earlier area = bigger = better
        for areas in self.board.areas:
            # check if any of the beneficial moves are in the area
            for move in beneficial:
                log(f"Checking for area of size {target}, found area of size {len(areas)}")
                # if the move is in the area and the size of the area is bigger than what we are looking for we are good
                if move in areas and len(areas) >= target:
                    log(f"Return move: {move.x},{move.y}")
                    return move
                # move is either not in the area or not big enough
                # TODO: can optimize this, break out early
                log (f"move: {move.x},{move.y} not accepted")
        # none of the moves take us to an area that is currently big enough
        # we check if any of the moves takes us to an area that can potentially open up to a suitable size
        for move in beneficial:
            turns, newsize = self.board.turns_to_open(move)
            log(f"Checking for area of size {target}, found area of size {newsize} after {turns} turns")
            # if  the size that the area opens up to is big enough
            if newsize >= target:
                # find the area in which the move belongs in
                # then we ensure that the current size of the area is big enough to hold us while we wait for the area to open
                for areas in self.board.areas:
                    if move in areas and len(areas) >= turns:
                        log(f"Return move: {move.x},{move.y}")
                        return move
            log (f"move: {move.x},{move.y} not accepted")
        # if we return none of our moves leads to an area that is big enough and none of our moves lead to an area that can expand to the size we need
        return None

    def basic_move(self):
        # keep track of all the possible moves (potentially risky)
        moves = self.board.possible_moves()
        # keep track of all the moves that cannot lead to death 
        moves_no_death = self.board.possible_moves_no_death()
        log(f"Possible Moves: {[self.board.my_snake.head.direction(x) for x in moves]}")
        log(f"Possible Moves No Death: {[self.board.my_snake.head.direction(x) for x in moves_no_death]}")

        # the head of the snake to build the potential moves out of
        head = self.board.my_snake.head
        # position of the head if we go up,down,left,right
        head_up = head.up()
        head_down = head.down()
        head_left = head.left()
        head_right = head.right()

        # no moves so dont waste time
        if not moves:
            return UP

        # we go for our tail 
        closestFood = self.board.my_snake.tail
        # if we are smaller than average snek or we are hungry, we go for food instead of our tail
        #if (self.board.my_snake.length < self.board.average_snake_size()) or self.board.my_snake.health < (self.board.height + self.board.width):
        if (self.board.my_snake.length <= (self.board.longest_snake_size() + 1)) or self.board.my_snake.health < (self.board.height + self.board.width):
            closestFood = self.board.closest_food()
        log(f"Closest food: ({closestFood.x},{closestFood.y})")

        # any move that brings us closer to food/tail goes in beneficial
        beneficial = []
        # we want the new area to be big enough to contain the entire snake
        target = self.board.my_snake.length
        # if we are bigger than the remaining spaces, we ignore target so set it to 0
        if target > self.board.free_spaces:
            target = 0

        # check through the safe moves first 
        if moves_no_death:
            # if the direction is in the safe moves list and the direction brings us closer to tail/food we add it to beneficial
            if (head_right in moves_no_death) and (self.board.my_snake.head.x < closestFood.x):
                beneficial.append(head_right)
            elif (head_left in moves_no_death) and (self.board.my_snake.head.x > closestFood.x):
                beneficial.append(head_left)
            if (head_down in moves_no_death) and (self.board.my_snake.head.y < closestFood.y):
                beneficial.append(head_down)
            elif (head_up in moves_no_death) and (self.board.my_snake.head.y > closestFood.y):
                    beneficial.append(head_up)
            # if there exists a beneficial move, we take it
            if beneficial:
                log(f"Beneficial Safe Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                # we find the best move out of the beneficial moves
                move_to_take = self.findBestMove(beneficial, target)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
            # if health is greater than threshold then dont take a riskier move and just take the best safe move
            if self.board.my_snake.health >= (self.board.height + self.board.width):
                log(f"Nothing beneficial and not starving")
                # pick the best out of all the safe moves
                move_to_take = self.findBestMove(moves_no_death, target)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
        # moves is not empty
        log("Making a risky move")
        # clear list of beneficial moves 
        beneficial.clear()
        # we take a potentially risky move and first look for risky moves that lead us closer to the food
        # if the direction leads us closer to food we add it to beneficial
        if (head_right in moves) and (self.board.my_snake.head.x < closestFood.x):
            beneficial.append(head_right)
        elif (head_left in moves) and (self.board.my_snake.head.x > closestFood.x):
            beneficial.append(head_left)
        if (head_down in moves) and (self.board.my_snake.head.y < closestFood.y):
            beneficial.append(head_down)
        elif (head_up in moves) and (self.board.my_snake.head.y > closestFood.y):
            beneficial.append(head_up)
        # if there is a beneficial move we take that since it brings us closer to goal
        if beneficial:
            log(f"Beneficial Risky Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
            move_to_take = self.findBestMove(beneficial, target)
            if move_to_take != None:
                return self.board.my_snake.head.direction(move_to_take)
        # no beneficial moves so just take the best move
        move_to_take = self.findBestMove(moves, target)
        if move_to_take != None:
            return self.board.my_snake.head.direction(move_to_take)
        # none of the moves lead to a suitable area so we just random
        log(f"Dont know what to do so returning random move: {self.board.my_snake.head.direction(random.choice(moves))}")
        return self.board.my_snake.head.direction(random.choice(moves))