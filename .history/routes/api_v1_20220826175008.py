# -*- coding: utf-8 -*-
from flask_restful import Api
from resources import user

#api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

api.add_resource(UserApi, "/user")