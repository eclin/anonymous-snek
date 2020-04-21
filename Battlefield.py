
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
        return Coord(x, y-1)

    def down(self):
        return Coord(x, y+1)

    def left(self):
        return Coord(x-1, y)

    def right(self):
        return Coord(x+1, y)

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
                self.all_snakes.append(Snake(s))

    # given the game data, this will update the board
    def update(self, data):
        self.food = []
        for f in data['board']['food']:
            self.food.append(Coord(f['x'], f['y']))

    def out_of_bounds(self, p):
        if p.x < 0 or p.x >= self.width or p.y < 0 or p.y >= self.height:
            return True
        return False

    # return possible moves given a position (default to your head)
    # moves returned could still lead to death
    def possible_moves(self, point=None):
        if point is None:
            point = self.my_snake.head
        moves = {
            UP: point.up(),
            DOWN: point.down(),
            LEFT: point.left(),
            RIGHT: point.right(),
        }
        for d in DIRECTIONS:
            if self.out_of_bounds(moves[d]):
                moves.pop(d)

        # Avoid crashing into other snake bodies/your own body
        for s in self.other_snakes:
            for d in DIRECTIONS:
                if moves[d] in s.body:
                    moves.pop(d)
        
        for d in DIRECTIONS:
            if self.my_snake.length > 1 and moves[d] == self.my_snake.body[1]:
                moves.pop(d)
        
        return [moves[d] for d in DIRECTIONS]

    def possible_moves_no_death(self, point=self.my_snake.head):
        moves = self.possible_moves()
        new_moves = []
        # check if can collide head on with another equal sized or longer snake
        for s in self.other_snakes:
            other_moves = s.possible_moves()
            for m in moves:
                if m not in other_moves:
                    new_moves.append(m)

        return new_moves


class Snake(object):
    min_length = 3

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

    # returns possible moves of the snake. Does not take into account bad moves.
    def possible_moves(self):
        return [head.up(), head.down(), head.left(), head.right()]
