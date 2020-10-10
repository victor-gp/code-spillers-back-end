"""
Define the REST verbs relative to the users
"""

from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from util import parse_params


class RecipesResource(Resource):
    """ Verbs relative to the Recipes """


    @staticmethod
    @swag_from("../swagger/recipes/POST.yml")
    def post():
        """ Return a list of K recipes based on the sent ingredients """
        wip_message = "hello foodie! wait a couple hours before we properly set up the API"
        return jsonify({"recipes": wip_message})
