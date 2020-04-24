import random
from Battlefield import *
from Log import log
import math

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

    def find_best_move(self,urgent, move_list, target):
        # since the areas are sorted in decreasing size, the best move will be the move that appears
        # in the earliest area since earlier area = bigger = better
        area_containing_point = [] # list of areas
        move_to_take = [] # list of (moves, score)
        best = (None, -math.inf)
        for areas in self.board.areas:
            # check if any of the moves are in the area
            for move in move_list:
                log(f"Checking for area of size {target}, found area of size {len(areas)}")
                # if the move is in the area and the size of the area is bigger than what we are looking for we are good
                if move in areas:
                    if len(areas) >= target:
                        log(f"Return move: {move.x},{move.y}")
                        area_containing_point.append(areas)
                        move_to_take.append(move,len(areas))
                        break
                    # area is not big enough
                    log (f"move: {move.x},{move.y} not accepted")
                    break
        for m in range(len(move_to_take)):
            another_snek = False
            for s in self.board.other_snakes:
                moves = {
                    UP: self.board.my_snake.head.up(),
                    DOWN: self.board.my_snake.head.down(),
                    LEFT: self.board.my_snake.head.left(),
                    RIGHT: self.board.my_snake.head.right(),
                }
                for i in moves:
                    if s.moves[i] in area_containing_point[m]:
                        move_to_take[m][1] -= int(s.length/4)
                        another_snek = True
            if another_snek == False:
                move_to_take[m][1] += 50
        for m in move_to_take:
            if m[1] > best[1]:
                best = m
        return best[0]        

    def get_to_food_first(self, food_location):
        our_distance = food_location.distance(self.board.my_snake.head)
        for s in self.board.other_snakes:
            if food_location.distance(s.head) < our_distance:
                return False
        return True

    def move_towards_food(self, moves):
        food_location = self.board.closest_food()
        if not self.get_to_food_first(food_location):
            return self.move_to_stall(moves)
        log(f"move towards food ({food_location.x},{food_location.y})")
        # keep track of all the moves that cannot lead to death 
        moves_no_death = self.board.possible_moves_no_death()
        log(f"Possible Moves No Death: {[self.board.my_snake.head.direction(x) for x in moves_no_death]}")
        # any move that brings us closer to food goes in beneficial
        beneficial = []
        not_beneficial = []
        urgent = self.board.my_snake.health < self.board.height + self.board.width
        # check through the safe moves first 
        if moves_no_death:
            # if the direction is in the safe moves list and the direction brings us closer to tail/food we add it to beneficial
            if (moves[RIGHT] in moves_no_death) and (self.board.my_snake.head.x < food_location.x):
                beneficial.append(moves[RIGHT])
            elif (moves[LEFT] in moves_no_death) and (self.board.my_snake.head.x > food_location.x):
                beneficial.append(moves[LEFT])
            if (moves[DOWN] in moves_no_death) and (self.board.my_snake.head.y < food_location.y):
                beneficial.append(moves[DOWN])
            elif (moves[UP] in moves_no_death) and (self.board.my_snake.head.y > food_location.y):
                    beneficial.append(moves[UP])
            # if there exists a beneficial move, we take it
            if beneficial:
                # we want the new area to be big enough to contain the entire snake
                target = self.board.my_snake.length
                # if we are bigger than the remaining spaces, we ignore target so set it to 0
                if target > self.board.free_spaces:
                    target = 0
                log(f"Beneficial Safe Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                # we find the best move out of the beneficial moves

                #if urgent: do something more deseperate

                move_to_take = self.find_best_move(urgent, beneficial, target)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
            not_beneficial = (list(set(moves_no_death) - set(beneficial)))
        if not urgent:
            return self.move_to_stall(moves)
        risky_moves = self.board.risky_moves()
        risky_moves = (list(set(moves_no_death) - set(risky_moves)))
        if risky_moves:
            beneficial.clear()    
            if (moves[RIGHT] in risky_moves) and (self.board.my_snake.head.x < food_location.x):
                beneficial.append(moves[RIGHT])
            elif (moves[LEFT] in risky_moves) and (self.board.my_snake.head.x > food_location.x):
                beneficial.append(moves[LEFT])
            if (moves[DOWN] in risky_moves) and (self.board.my_snake.head.y < food_location.y):
                beneficial.append(moves[DOWN])
            elif (moves[UP] in risky_moves) and (self.board.my_snake.head.y > food_location.y):
                beneficial.append(moves[UP])
            # if there is a beneficial move we take that since it brings us closer to goal
            if beneficial:
                target = self.board.my_snake.length
                # if we are bigger than the remaining spaces, we ignore target so set it to 0
                if target > self.board.free_spaces:
                    target = 0
                log(f"Beneficial Risky Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                
                #if urgent: do something more deseperate

                move_to_take = self.find_best_move(urgent, beneficial, target)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
                target = 0
                return self.board.my_snake.head.direction(self.find_best_move(urgent, beneficial, target))
        return self.board.my_snake.head.direction(random.choice(moves_no_death))
    
    def move_to_stall(self, moves):
        log(f"move to stall")
        # keep track of all the moves that cannot lead to death 
        moves_no_death = self.board.possible_moves_no_death()
        log(f"Possible Moves No Death: {[self.board.my_snake.head.direction(x) for x in moves_no_death]}")
        tail_location = self.board.my_snake.tail
        beneficial = []
        if moves_no_death:
            # if the direction is in the safe moves list and the direction brings us closer to tail/food we add it to beneficial
            if (moves[RIGHT] in moves_no_death) and (self.board.my_snake.head.x < tail_location.x):
                beneficial.append(moves[RIGHT])
            elif (moves[LEFT] in moves_no_death) and (self.board.my_snake.head.x > tail_location.x):
                beneficial.append(moves[LEFT])
            if (moves[DOWN] in moves_no_death) and (self.board.my_snake.head.y < tail_location.y):
                beneficial.append(moves[DOWN])
            elif (moves[UP] in moves_no_death) and (self.board.my_snake.head.y > tail_location.y):
                    beneficial.append(moves[UP])
            # if there exists a beneficial move, we take it
            if beneficial:
                # we want the new area to be big enough to contain the entire snake
                target = self.board.my_snake.length
                # if we are bigger than the remaining spaces, we ignore target so set it to 0
                if target > self.board.free_spaces:
                    target = 0
                log(f"Beneficial Safe Moves: ({[self.board.my_snake.head.direction(x) for x in beneficial]})")
                # we find the best move out of the beneficial moves

                move_to_take = self.find_best_move(False, beneficial, target)
                if move_to_take != None:
                    return self.board.my_snake.head.direction(move_to_take)
        if not moves_no_death:
            return UP
        return self.board.my_snake.head.direction(self.find_best_move(False, moves_no_death, target))

    def basic_move(self):
        # keep track of all the possible moves (potentially risky)
        moves = self.board.possible_moves()
        log(f"Possible Moves: {[self.board.my_snake.head.direction(x) for x in moves]}")

        moves = {
            UP: self.board.my_snake.head.up(),
            DOWN: self.board.my_snake.head.down(),
            LEFT: self.board.my_snake.head.left(),
            RIGHT: self.board.my_snake.head.right(),
        }

        #if (self.board.my_snake.length < self.board.average_snake_size()) or self.board.my_snake.health < (self.board.height + self.board.width):
        # we want to be the biggest on the board
        if (self.board.my_snake.length <= (self.board.longest_snake_size())) or self.board.my_snake.health < (self.board.height + self.board.width):
            return self.move_towards_food(moves)
        else:
            return self.move_to_stall(moves)