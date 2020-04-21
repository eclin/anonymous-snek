
from Battlefield import *

class BattfieldTest():
    def __init__(self):
        self.coord_test = CoordTest()
        self.board_test = BoardTest()
        self.snake_test = SnakeTest()

    def test(self):
        self.coord_test.test()
        self.board_test.test()
        self.snake_test.test()
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

class BoardTest():
    def __init__(self):
        super().__init__()

    def test(self):
        pass

class SnakeTest():
    def __init__(self):
        super().__init__()

    def test(self):
        pass
