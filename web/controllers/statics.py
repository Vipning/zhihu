from flask import Blueprint,send_from_directory
from application import app
route_static = Blueprint('statics', __name__)

#图片加载
@route_static.route("/<filename>")
def index(filename):
    return send_from_directory(app.root_path + "/web/statics/images/",filename)