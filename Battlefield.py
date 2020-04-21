import math

LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'
DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

class Coord(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def up(self):
        return Coord(self.x, self.y-1)

    def down(self):
        return Coord(self.x, self.y+1)

    def left(self):
        return Coord(self.x-1, self.y)

    def right(self):
        return Coord(self.x+1, self.y)

    def distance(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

    def direction(self, p):
        if self.up() == p:
            return UP
        if self.down() == p:
            return DOWN
        if self.right() == p:
            return RIGHT
        if self.left() == p:
            return LEFT

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __ne__(self, p):
        return not self.__eq__(p)

class Board(object):
    # data is the entire game json dictionary.
    def __init__(self, data):
        # parse the data
        self.id = data['game']['id']
        self.height = data['board']['height']
        self.width = data['board']['width']
        self.food = []
        for f in data['board']['food']:
            self.food.append(Coord(f['x'], f['y']))
        self.my_snake = Snake(data['you'])
        self.other_snakes = []
        for s in data['board']['snakes']:
            if s['id'] != self.my_snake.id:
                self.other_snakes.append(Snake(s))

    # given the game data, this will update the board
    def update(self, data):
        self.food = []
        for f in data['board']['food']:
            self.food.append(Coord(f['x'], f['y']))
        self.my_snake.update(data['you'])
        for s in data['board']['snakes']:
            curID = s['id']
            if curID != self.my_snake.id:
                for o in self.other_snakes:
                    if curID == o.id:
                        o.update(s)

    def out_of_bounds(self, p):
        if p.x < 0 or p.x >= self.width or p.y < 0 or p.y >= self.height:
            return True
        return False

    # returns coord of closest food to your snake head
    def closest_food(self):
        low = self.height + self.width
        p = self.food[0]
        for f in self.food:
            if self.my_snake.head.distance(f) < low:
                p = f
                low = self.my_snake.head.distance(f)
        return p

    # return possible moves given a position (default to your head)
    # moves returned could still lead to death (like head on head)
    def possible_moves(self):
        moves = {
            UP: self.my_snake.head.up(),
            DOWN: self.my_snake.head.down(),
            LEFT: self.my_snake.head.left(),
            RIGHT: self.my_snake.head.right(),
        }
        for d in DIRECTIONS:
            if self.out_of_bounds(moves[d]):
                moves.pop(d)

        # Avoid crashing into other snake bodies/your own body,
        # except for the tail if it were to move
        for s in self.other_snakes:
            for d in DIRECTIONS:
                if d in moves and moves[d] in s.body:
                    # if its to a tail spot and the tail will move, then its ok
                    if moves[d] == s.tail and not s.will_extend:
                        continue
                    moves.pop(d)
        
        for d in DIRECTIONS:
            if d in moves and moves[d] in self.my_snake.body:
                moves.pop(d)
        
        return [moves[d] for d in moves]

    def possible_moves_no_death(self):
        moves = self.possible_moves()
        new_moves = []
        other_moves = []
        # check if can collide head on with another equal sized or longer snake
        for s in self.other_snakes:
            if s.length >= self.my_snake.length:
                for m in s.possible_moves():
                    other_moves.append(m)
        for m in moves:
            if m not in other_moves:
                new_moves.append(m)

        return new_moves


class Snake(object):
    # data is a snake dict, not the entire game dict
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.health = data['health']
        self.body = []
        for b in data['body']:
            self.body.append(Coord(b['x'], b['y']))
        self.head = self.body[0]
        self.tail = self.body[-1]
        self.length = len(self.body)
        self.will_extend = True
        self.just_ate = True

    # updates a snake
    def update(self, data):
        self.health = data['health']

        first = Coord(data['body'][0]['x'], data['body'][0]['y'])
        last = Coord(data['body'][-1]['x'], data['body'][-1]['y'])
        self.body.insert(0, first)
        if len(data['body']) > self.length:
            # just ate a food -> pop back, add new back
            self.body.pop(-1)
            self.body.append(last)
            self.just_ate = True
            self.will_extend = True

        self.head = self.body[0]
        self.tail = self.body[-1]
        self.length = len(self.body)

    # returns possible moves of the snake. Does not take into account bad moves.
    def possible_moves(self):
        return [self.head.up(), self.head.down(), self.head.left(), self.head.right()]
