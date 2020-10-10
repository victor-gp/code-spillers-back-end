"""
Defines the blueprint for the recipes
"""
from flask import Blueprint
from flask_restful import Api

from resources import RecipesResource

RECIPES_BLUEPRINT = Blueprint("recipes", __name__)
Api(RECIPES_BLUEPRINT).add_resource(
    RecipesResource, "/recipes/"
)
