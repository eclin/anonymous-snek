import random
import cherrypy

from Snake import Snake

class RandomSnake(Snake):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start(self):
        data = cherrypy.request.json
        print("START")
        print(data)
        return {"color": "#888888", "headType": "bendr", "tailType": "regular"}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json

        possible_moves = ["up", "down", "left", "right"]
        move = random.choice(possible_moves)

        print(data)
        print(f"MOVE: {move}")
        return {"move": move}