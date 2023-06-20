import responder

from . import layouts
from . import callbacks
from .server import app

api = responder.API()
api.mount("", app.server)
api.add_route("/static/", static=True)
api.run(debug=True)
