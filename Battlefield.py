import copy
from Log import log

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
        if p is None:
            return False
        return self.x == p.x and self.y == p.y

    def __ne__(self, p):
        return not self.__eq__(p)

    def __hash__(self):
        strx = str(self.x * 100)
        stry = str(self.y * 100)
        return (strx + stry).__hash__()

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
        self.areas = self.compute_areas()
        self.free_spaces = (self.height * self.width) - len(self.my_snake.body)
        self.free_spaces -= sum([len(b.body) for b in self.other_snakes])

    # given the game data, this will update the board
    def update(self, data):
        self.food = []
        for f in data['board']['food']:
            self.food.append(Coord(f['x'], f['y']))
        self.my_snake.update(data['you'])
        updated_snakes = []
        for s in data['board']['snakes']:
            curID = s['id']
            if curID != self.my_snake.id:
                for o in self.other_snakes:
                    if curID == o.id:
                        o.update(s)
                        updated_snakes.append(curID)
        # if a snake was not updated, it means it died
        live_snakes = []
        for s in self.other_snakes:
            if s.id in updated_snakes:
                live_snakes.append(s)
        self.other_snakes = live_snakes
        self.areas = self.compute_areas()
        self.free_spaces = (self.height * self.width) - len(self.my_snake.body)
        self.free_spaces -= sum([len(b.body) for b in self.other_snakes])

    def average_snake_size(self):
        return int(sum([len(b.body) for b in self.other_snakes]) / len(self.other_snakes))
    
    def longest_snake_size(self):
        max = 0
        for snake in self.other_snakes:
            if len(snake.body) > max:
                max = len(snake.body)
        return max

    def compute_areas(self):
        # create height x width 2D array of all 0s
        grid = [[0] * self.width for x in range(self.height)]

        # For each snake body, mark the grid with a 1
        for s in self.other_snakes:
            for b in s.body:
                grid[b.y][b.x] = 1
        for b in self.my_snake.body:
            grid[b.y][b.x] = 1
        
        areas = []
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == 1:
                    continue
                size, area = self.compute_area(grid, Coord(x, y))
                areas.append(area)
        areas.sort(key=lambda x: len(x), reverse=True)
        return areas

    # Given a grid and Coord p, returns the size of the area that p is in
    # along with an array of Coords representing that area
    # grid must be 0 if free, 1 if occupied.
    # will set all points of that area to 1.
    # if p is not a free point, returns 0, []
    def compute_area(self, g, p, make_copy=False):
        if make_copy:
            grid = copy.deepcopy(g)
        else:
            grid = g
        if grid[p.y][p.x] == 1:
            return 0, []
        grid[p.y][p.x] = 1
        area = [p]
        stack = [p.up(), p.down(), p.left(), p.right()]
        while len(stack) > 0:
            top = stack.pop(-1)
            if self.out_of_bounds(top):
                continue
            if grid[top.y][top.x] == 1:
                continue
            area.append(top)
            grid[top.y][top.x] = 1
            stack += [top.up(), top.down(), top.left(), top.right()]
        return len(area), area
                
    # Given any Coord p in an area (not a snake), this returns the number of turns it
    # takes for the area to open up (increase in size) and the size of the
    # new area. If there is only one area, it can't open up and will return -1, -1
    def turns_to_open(self, p):
        if len(self.areas) == 1:
            return -1, -1
        orig_size = 0
        for a in self.areas:
            if p in a:
                orig_size = len(a)
                break

        all_snakes = self.other_snakes + [self.my_snake]

        # remove the ends of all snakes and recompute area
        # if bigger, then return the turns and new size
        # if not, then repeat
        max_len = 0
        for s in all_snakes:
            max_len = max(s.length, max_len)
        
        grid = [[0] * self.width for x in range(self.height)]
        for s in all_snakes:
            for b in s.body:
                grid[b.y][b.x] = 1

        turn = 1
        while turn <= max_len:
            for s in all_snakes:
                if s.length >= turn:
                    grid[s.body[-turn].y][s.body[-turn].x] = 0
            cur_size, cur_area = self.compute_area(grid, p, make_copy=True)
            if cur_size > orig_size:
                return turn, cur_size
            turn += 1
        
        # should never reach here
        log("Should never reach here")
        return -1, -1
            
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
                if moves[d] == self.my_snake.tail and not self.my_snake.will_extend:
                    continue
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
        self.will_extend = False
        self.just_ate = False

        first = Coord(data['body'][0]['x'], data['body'][0]['y'])
        last = Coord(data['body'][-1]['x'], data['body'][-1]['y'])
        self.body.insert(0, first)
        if len(data['body']) >= len(self.body): #self.size_on_board():
            log(f"Ate, new tail: ({last.x},{last.y})")
            # just ate a food -> pop back, add new back
            self.body.pop(-1)
            self.body.append(last)
            self.just_ate = True
            self.will_extend = True
        else:
            self.body.pop(-1)

        self.head = self.body[0]
        self.tail = self.body[-1]
        self.length = len(self.body)
        log(f"Upated len:{self.length}, actual len:{len(data['body'])}")

    def size_on_board(self):
        return len({x for x in self.body})

    # returns possible moves of the snake. Does not take into account bad moves.
    def possible_moves(self):
        return [self.head.up(), self.head.down(), self.head.left(), self.head.right()]

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)
