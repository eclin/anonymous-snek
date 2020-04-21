import cherrypy

from tests.BattlefieldTest import BattfieldTest

class Snake():
    @cherrypy.expose
    def index(self):
        return "Your Battlesnake is alive!"

    @cherrypy.expose
    def ping(self):
        return "pong"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        data = cherrypy.request.json
        print("END")
        return "ok"

    @cherrypy.expose
    def test(self):
        battlefield_test = BattfieldTest()
        battlefield_test.test()
        return 'Done Tests'
