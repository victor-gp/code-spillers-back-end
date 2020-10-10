import json
import re
import requests
import threading

ingredLock = threading.RLock()
posLock = threading.RLock()
recipeLock = threading.RLock()



def recipesByIngredients(ingredientsList, maxRecpts='20', ranking='2', ignoreParty='true'):
    '''
    Inputs:
        ingredientsList : list of incredients
        maxRecpts : maximum number of receipts to generate
        ranking : '1' use maximum ingredients missing, '2' - use minimum ingredients missing for generating recipes
        ignoreParty : 'false' - does not ignore basic materials like water , 'true' ignores
    Output:
        response from API converted into JSON
    '''
    ingredLock.acquire()  ## maybe delete

    maxRecpts = str(maxRecpts)
    ranking = str(ranking)
    ignoreParty = str(ignoreParty)
    ingredientsList = '%2C'.join(ingredientsList)

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"
    querystring = {"number": maxRecpts, "ranking": ranking, "ignorePantry": ignoreParty, "ingredients": ingredientsList}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "f550b025c9mshf7e779815980f33p1a185djsn190432425332"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    ingredLock.release()  ## make be delete
    return response




def postProcess(data, ingredientsList):
    '''
    Input:
        data : output received from API as JSON file
        ingredientsList: original list with Ingredients
    Output:
        Yet not decided, so far it is list of dictionaries
    '''
    posLock.acquire()  ## maybe delete
    missedFlag = False

    output = []

    for raw in data:
        ingrdtsList = ingredientsList.copy()

        ingredientRecord = list()

        for missIngrdt in raw['missedIngredients']:
            misses = missIngrdt['name'].split(" ")
            missedFlag = True
            for miss in misses:
                if miss in ingrdtsList:
                    ingrdtsList.pop(ingrdtsList.index(miss))
                    missedFlag = False
                    break
            if missedFlag == True:
                break
            missed = missIngrdt['name']

            ingredientRecord.append(missed)

        for usedIngred in raw['usedIngredients']:
            ingred = usedIngred['name']
            ingredientRecord.append(ingred)

        if missedFlag == False:
            record = {'id': raw['id']}
            record['title'] = raw['title']
            record['ingredients'] = ingredientRecord
            output.append(record)
    posLock.release()
    return output




def getStepwiseRecipy(data, stepBreakdown='true'):
    '''
    Input:
        data:
    '''

    recipeLock.acquire()

    output = list()

    for raw in data:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%d/analyzedInstructions" % (
        raw['id'])

        querystring = {"stepBreakdown": stepBreakdown}
        print(querystring)
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
        }

        response = requests.request("GET", url, headers=headers, params=querystring, )

        response = response.json()

        if len(response) == 0:
            continue
        raw['steps'] = [record['step'] for record in response[0]['steps']]
        output.append(raw)
    recipeLock.release()
    return output


imgDownloadLock = threading.RLock()


def downloadImage(ID):
    '''
    Under construction
    '''
    imgDownloadLock.acquire()

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%d/information" % (ID)

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
    }

    response = requests.request("GET", url, headers=headers)

    response = response.json()
    image_url = response['image']
    imgDownloadLock.release()
    return image_url


response = recipesByIngredients(
    ['apples', 'bananas', 'mango', 'milk', 'ginger', 'meat', 'eggs', 'water', 'caramels', 'juice', 'spinach',
     'cucumber', 'garlic', 'oil', 'baking soda', 'flour',
     'potatoes', 'tomatoes', 'onion'])

data=response.json()

ingredientsList=['apples','bananas','mango','milk','ginger','meat','eggs','water','caramels','juice','spinach','cucumber','garlic','oil','baking soda','flour',
                              'potatoes','tomatoes','onion']

processed=postProcess(data,ingredientsList)
pposData=getStepwiseRecipy(processed)


print(data)
print(processed)
print(pposData)