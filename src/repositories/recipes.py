""" Defines the Recipes repository """

#from util import recipesByIngredients

class RecipesRepository:
    """ A repository for handling requests to the recipes API """

    @staticmethod
    def get_by_ingredients(ingredients):
        # todo: your main method goes here, assume ingredients is a list of strings

        api_response_stub = "hello foodie! wait a couple hours before we properly set up the API"

        return api_response_stub

        """

        how to integrate function.py

        - take all of the code at root indentation level and make a main method
        - import the main method in util/__init__.py
        - call it from here
            - in: list of ingredient strings
            - out: probably JSON, whatever the API returns
                but if it's a bother, we can easily convert to JSON in src/resources/recipes.py

        """
