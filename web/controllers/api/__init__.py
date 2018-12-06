from flask import Blueprint

route_api =Blueprint('api_page',__name__)
from web.controllers.api.member import *
from web.controllers.api.question import *
from web.controllers.api.answer import *
from web.controllers.api.message import *