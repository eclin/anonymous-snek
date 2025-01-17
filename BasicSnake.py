import random
import cherrypy
import time

from Snake import Snake
from basicSinglePlayer import BasicStrategy
from tests.BattlefieldTest import BattfieldTest
from Log import log

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
        log("START")
        log(data)
        return {"color": "#9BC4E2", "headType": "bendr", "tailType": "bolt"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        start = time.time()
        data = cherrypy.request.json
        snake_id = data['you']['id']
        self.strategy[snake_id].update(data)
        move = self.strategy[snake_id].basic_move()
        end = time.time()
        log(f"Time:{end-start}")
        log(data)
        log(f"MOVE: {move}")
        return {"move": move}
