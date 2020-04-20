import os
import random
import cherrypy

from RandomSnake import RandomSnake
from BasicSnake import BasicSnake


if __name__ == "__main__":
    basic = BasicSnake()
    random = RandomSnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.tree.mount(random, '/random')
    cherrypy.quickstart(basic)
