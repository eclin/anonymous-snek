import json

from Battlefield import *

class BattfieldTest():
    def __init__(self):
        self.coord_test = CoordTest()
        self.board_snake_test = BoardSnakeTest()

    def test(self):
        self.coord_test.test()
        self.board_snake_test.test()
        print("End of tests")


class CoordTest():
    def __init__(self):
        self.p = Coord(1, 1)

    def test(self):
        assert self.p.up() == Coord(1, 0)
        assert self.p.down() == Coord(1, 2)
        assert self.p.left() == Coord(0, 1)
        assert self.p.right() == Coord(2, 1)
        assert self.p.direction(Coord(1, 0)) == UP
        assert self.p.direction(Coord(1, 2)) == DOWN
        assert self.p.direction(Coord(0, 1)) == LEFT
        assert self.p.direction(Coord(2, 1)) == RIGHT
        assert self.p.distance(Coord(10, 10)) == 18
        assert self.p == Coord(1, 1)
        assert self.p != Coord(6, 9)

class BoardSnakeTest():
    def __init__(self):
        f = open("tests/exampleboard.txt")
        data = json.load(f)
        self.board = Board(data)

    def test(self):
        # assert board properties
        assert self.board.id == '565f9a41-ca40-44dc-979a-212470145779'
        assert self.board.height == 11
        assert self.board.width == 11
        assert self.board.food == [Coord(2, 4), Coord(6, 1)]
        assert self.board.free_spaces == 115

        # assert your own snake properties
        assert self.board.my_snake.id == 'gs_J7YmyRgTFCPHcbKG3fyBrBRD'
        assert self.board.my_snake.name == 'Start Snek'
        assert self.board.my_snake.health == 98
        assert self.board.my_snake.body == [Coord(6, 4), Coord(6, 5), Coord(6, 6)]
        assert self.board.my_snake.head == Coord(6, 4)
        assert self.board.my_snake.tail == Coord(6, 6)
        assert self.board.my_snake.length == 3
        assert self.board.my_snake.will_extend == True # starting snakes always have this True
        assert self.board.my_snake.just_ate == True

        # assert other snake properties
        assert len(self.board.other_snakes) == 1
        assert self.board.other_snakes[0].id == 'gs_J7YmyRgTFCPHcbKG3fyBrBRP'
        assert self.board.other_snakes[0].name == 'Snake 2'
        assert self.board.other_snakes[0].health == 93
        assert self.board.other_snakes[0].body == [Coord(5, 5), Coord(5, 6), Coord(5, 7)]
        assert self.board.other_snakes[0].head == Coord(5, 5)
        assert self.board.other_snakes[0].tail == Coord(5, 7)
        assert self.board.other_snakes[0].length == 3
        assert self.board.other_snakes[0].will_extend == True
        assert self.board.other_snakes[0].just_ate == True

        # assert battlefield functions
        assert self.board.out_of_bounds(Coord(3, 4)) == False
        assert self.board.out_of_bounds(Coord(-3, 4)) == True
        assert self.board.out_of_bounds(Coord(1, 14)) == True
        assert self.board.closest_food() == Coord(6, 1)
        moves = self.board.possible_moves()
        assert len(moves) == 3
        assert Coord(5, 4) in moves and Coord(6, 3) in moves and Coord(7, 4) in moves
        moves_no_death = self.board.possible_moves_no_death()
        assert len(moves_no_death) == 2
        assert Coord(6, 3) in moves_no_death and Coord(7, 4) in moves_no_death

        # assert snake functions
        moves = self.board.my_snake.possible_moves()
        assert len(moves) == 4
        assert Coord(5, 4) in moves and Coord(6, 3) in moves 
        assert Coord(7, 4) in moves and Coord(6, 5) in moves

        # test the update function!!
        f = open("tests/exampleupdate.txt")
        data = json.load(f)
        self.board.update(data)

        # assert board properties
        assert self.board.id == '565f9a41-ca40-44dc-979a-212470145779'
        assert self.board.height == 11
        assert self.board.width == 11
        assert self.board.free_spaces == 115
        food = self.board.food
        assert Coord(2, 4) in food 
        assert Coord(6, 1) in food 
        assert Coord(7, 3) in food

        # assert your own snake properties
        assert self.board.my_snake.id == 'gs_J7YmyRgTFCPHcbKG3fyBrBRD'
        assert self.board.my_snake.name == 'Start Snek'
        assert self.board.my_snake.health == 97
        assert self.board.my_snake.body == [Coord(6, 3), Coord(6, 4), Coord(6, 5)]
        assert self.board.my_snake.head == Coord(6, 3)
        assert self.board.my_snake.tail == Coord(6, 5)
        assert self.board.my_snake.length == 3
        assert self.board.my_snake.will_extend == False # starting snakes always have this True
        assert self.board.my_snake.just_ate == False

        # assert other snake properties
        assert len(self.board.other_snakes) == 1
        assert self.board.other_snakes[0].id == 'gs_J7YmyRgTFCPHcbKG3fyBrBRP'
        assert self.board.other_snakes[0].name == 'Snake 2'
        assert self.board.other_snakes[0].health == 92
        assert self.board.other_snakes[0].body == [Coord(5, 4), Coord(5, 5), Coord(5, 6)]
        assert self.board.other_snakes[0].head == Coord(5, 4)
        assert self.board.other_snakes[0].tail == Coord(5, 6)
        assert self.board.other_snakes[0].length == 3
        assert self.board.other_snakes[0].will_extend == False
        assert self.board.other_snakes[0].just_ate == False

        # assert battlefield functions
        assert self.board.closest_food() == Coord(7, 3)
        moves = self.board.possible_moves()
        assert len(moves) == 3
        assert Coord(5, 3) in moves and Coord(6, 2) in moves and Coord(7, 3) in moves
        moves_no_death = self.board.possible_moves_no_death()
        assert len(moves_no_death) == 2
        assert Coord(6, 2) in moves_no_death and Coord(7, 3) in moves_no_death

        # assert snake functions
        moves = self.board.my_snake.possible_moves()
        assert len(moves) == 4
        assert Coord(5, 3) in moves and Coord(6, 2) in moves 
        assert Coord(7, 3) in moves and Coord(6, 4) in moves

        self.board.my_snake.body.append(Coord(6, 5))
        assert self.board.my_snake.size_on_board() == 3

        # test the compute_areas function
        assert len(self.board.areas) == 1
        assert len(self.board.areas[0]) == 115
        f = open("tests/test_areas.txt")
        data = json.load(f)
        self.board = Board(data)
        assert self.board.free_spaces == 102
        assert len(self.board.areas) == 3
        assert len(self.board.areas[0]) == 55
        assert len(self.board.areas[1]) == 25
        assert len(self.board.areas[2]) == 22

        # test the turns_to_open function
        turns, size = self.board.turns_to_open(Coord(2, 3))
        print(turns)
        print(size)
        assert turns == 1
        assert size == 105
