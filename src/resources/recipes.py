"""
Define the REST verbs relative to the users
"""

from flasgger import swag_from
from flask.json import jsonify
from flask_restful import Resource
from flask_restful.reqparse import Argument

from repositories import RecipesRepository
from util import parse_params

import sys

class RecipesResource(Resource):
    """ Verbs relative to the Recipes """


    @staticmethod
    @parse_params(
        Argument("ingredients", location="json", type=str, action='append',
                 help="The list of ingredients.")
    )
    @swag_from("../swagger/recipes/POST.yml")
    def post(ingredients):
        """ Return a list of 3 recipes based on the sent ingredients """

        # debugging
        print('DEBUG: writing to STDERR works fine', file=sys.stderr)
        print( ", ".join(ingredients), file=sys.stderr )
        # takes a server reload to show up in the container output (just Ctrl+S here!)

        recipes = RecipesRepository.get_by_ingredients(ingredients)

        return jsonify({"recipes": recipes})


"""

before swagger rendering:

{
  "ingredients" : [
    "apples", "bananas", "mango", "milk", "ginger", "meat",
    "eggs", "water", "caramels", "juice", "spinach",
    "cucumber", "garlic", "oil", "baking soda", "flour",
    "potatoes", "tomatoes", "onion"]
}

expected input, after swagger rendering:

curl -X POST "http://127.0.0.1:3000/application/recipes/" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"ingredients\" : [ \"apples\", \"bananas\", \"mango\", \"milk\", \"ginger\", \"meat\", \"eggs\", \"water\", \"caramels\", \"juice\", \"spinach\", \"cucumber\", \"garlic\", \"oil\", \"baking soda\", \"flour\", \"potatoes\", \"tomatoes\", \"onion\"]}"

transformed input:

ingredients = [
    "apples", "bananas", "mango", "milk", "ginger", "meat",
    "eggs", "water", "caramels", "juice", "spinach",
    "cucumber", "garlic", "oil", "baking soda", "flour",
    "potatoes", "tomatoes", "onion"
]

"""
