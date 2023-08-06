import sys, os
import getopt
import tornado.wsgi
import tornado.httpserver
import tornado.ioloop

hostname = '127.0.0.1'
port = 80

opts, args = getopt.getopt(sys.argv[1:], "h:p:", [])
for o, a in opts:
    if o == '-h':
        hostname = a
    elif o == '-p':
        port = int(a)

path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

from uliweb.manage import make_simple_application
application = make_simple_application(project_dir=path)

container = tornado.wsgi.WSGIContainer(application)
http_server = tornado.httpserver.HTTPServer(container, xheaders=True)
http_server.listen(port, address=hostname)
tornado.ioloop.IOLoop.instance().start()

