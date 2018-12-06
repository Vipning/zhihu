from application import app
from web.controllers.api import route_api
from web.controllers.statics import route_static
app.register_blueprint(route_api,url_prefix='/api')
app.register_blueprint( route_static,url_prefix = "/statics" )
