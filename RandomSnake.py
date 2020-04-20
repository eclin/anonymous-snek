import random
import cherrypy

class RandomSnake(object):
    @cherrypy.expose
    def index(self):
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        return "pong"

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

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        data = cherrypy.request.json
        print("END")
        return "ok"