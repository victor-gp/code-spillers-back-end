"""
Define the REST verbs relative to the users
"""

from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import RecipesRepository
from util import parse_params


class RecipesResource(Resource):
    """ Verbs relative to the Recipes """


    @staticmethod
    @swag_from("../swagger/recipes/POST.yml")
    def post():
        """ Return a list of K recipes based on the sent ingredients """

        ingredients = [
            'apples', 'bananas', 'mango', 'milk', 'ginger', 'meat',
            'eggs', 'water', 'caramels', 'juice', 'spinach',
            'cucumber', 'garlic', 'oil', 'baking soda', 'flour',
            'potatoes', 'tomatoes', 'onion'
        ]

        recipes = RecipesRepository.get_by_ingredients(ingredients)

        return jsonify({"recipes": recipes})
