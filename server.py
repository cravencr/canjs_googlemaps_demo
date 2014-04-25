import tornado.ioloop
import tornado.web
import json
import os

class GeoPoint(object):
    def __init__(self, lat, lon):
        self.id = self.nextId()
        self.lat = lat;
        self.lon = lon;

    def nextId(self):
        global start_id
        start_id = start_id + 1
        return start_id

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        with open(os.path.dirname(__file__) + 'index.html', 'r') as file:
            self.write(file.read())

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('index.html')

class CSSHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('style.css')

class GeoPointHandler(tornado.web.RequestHandler):
    def get(self):
        global geopoints

        self.write(json.dumps([p.__dict__ for p in geopoints]))

    def post(self):
        lat = self.get_argument("lat", None)
        lon = self.get_argument("lon", None)
        if lat != None and lon != None:
            geopoints.append(GeoPoint(lat, lon))

    def put(self, id):
        self.write('ok')

    def delete(self, id):
        self.write('ok')

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/index.html", IndexHandler),
    (r"/geo.json", GeoPointHandler),
    (r"/style.css", CSSHandler)
])

geopoints = []
start_id = 1

if __name__ == "__main__":
    geopoints.append(GeoPoint('32.1', '-82.0'))
    application.listen(50123)
    tornado.ioloop.IOLoop.instance().start()
