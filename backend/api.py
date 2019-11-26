from flask import Blueprint
from flask_restful import Api, Resource

api_blueprint = Blueprint('api', __name__, url_prefix = '/api')

class Spam(Resource):
  def get(self):
    return { 'id': 42, 'name': 'Name' }

api = Api(api_blueprint)
api.add_resource(Spam, '/spam')
