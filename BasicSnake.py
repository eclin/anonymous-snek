import random
import cherrypy

from Snake import Snake
from basicSinglePlayer import BasicStrategy
from tests.BattlefieldTest import BattfieldTest

class BasicSnake(Snake):
    def __init__(self):
        self.strategy = {}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        data = cherrypy.request.json
        snake_id = data['you']['id']
        self.strategy[snake_id] = BasicStrategy(data)
        print("START")
        print(data)
        return {"color": "#888889", "headType": "bendr", "tailType": "sharp"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        snake_id = data['you']['id']
        self.strategy[snake_id].update(data)
        move = self.strategy[snake_id].basic_move()

        print(data)
        print(f"MOVE: {move}")
        return {"move": move}
