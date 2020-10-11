import json
import re
import requests
import threading

from flask import current_app as app

ingredLock = threading.RLock()
posLock = threading.RLock()
recipeLock = threading.RLock()
imgDownloadLock = threading.RLock()
processLocker = threading.RLock()



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
    # ingredLock.acquire()  ## maybe delete

    maxRecpts = str(maxRecpts)
    ranking = str(ranking)
    ignoreParty = str(ignoreParty)
    ingredientsList = '%2C'.join(ingredientsList)


    url = "https://webknox-recipes.p.rapidapi.com/recipes/findByIngredients"

    headers = {
        'x-rapidapi-host': "webknox-recipes.p.rapidapi.com",
        'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
    }


    querystring = {"number": maxRecpts, "ranking": ranking, "ignorePantry": ignoreParty, "ingredients": ingredientsList}


    response = requests.request("GET", url, headers=headers, params=querystring)

    # ingredLock.release()  ## make be delete
    return response



def lemmatize(text):
    '''
    Input: text data with words separated with commas
    Output: list of all available lemma (one per word)
    '''

    url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/lemma_extract/"

    querystring = {"text":text,}

    headers = {
        'x-rapidapi-host': "twinword-twinword-bundle-v1.p.rapidapi.com",
        'x-rapidapi-key': "f550b025c9mshf7e779815980f33p1a185djsn190432425332"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response=response.json()
    ingredientsList=[key for key,value in response['lemma'].items()]
    return ingredientsList


def getNutriotion(ID):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%d/nutritionWidget.json" % ID
    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "31d006966cmsh9614873845ef7d2p12bff3jsnd96e7b0355ba"
    }
    response = requests.request("GET", url, headers=headers)
    response = response.json()

    record = {'calories': response['calories']}
    record['carbs'] = response['carbs']
    record['fat'] = response['fat']
    record['protein'] = response['protein']
    return record



def getVideoByRecipe(recipeTitle):
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/videos/search"

    querystring = {"query": recipeTitle, "minLength": "00", "maxLength": "999", "offset": "0", "number": "1"}

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    if len(response['videos']) == 0:
        return 'none'
    video = response['videos'][0]['youTubeId']

    return 'youtube.com/watch?v=' + video



def postProcess(data, ingredientsList):
    '''
    Input:
        data : output received from API as JSON file
        ingredientsList: original list with Ingredients
    Output:
        list of dictionaries

    '''
    # posLock.acquire()  ## maybe delete
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

            lemmaInp = [ingredient for ingredient in ingredientRecord if len(ingredient.split(" ")) == 1]
            nonLemmaInp = [ingredient for ingredient in ingredientRecord if len(ingredient.split(" ")) > 1]

            lemmaInp = ' '.join(lemmaInp)
            ingredientRecord = lemmatize(lemmaInp)
            ingredientRecord.extend(nonLemmaInp)
            record['ingredients'] = ingredientRecord
            record['video_url'] = getVideoByRecipe(raw['title'])
            record['nutritions'] = getNutriotion(raw['id'])

            output.append(record)
    # posLock.release()
    return output



def downloadImage(ID):
    '''
    Input: integer ID of recipe
    Output: URL of image
    '''
    # imgDownloadLock.acquire()

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%d/information" % (ID)

    headers = {
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
    }

    response = requests.request("GET", url, headers=headers)

    response = response.json()
    image_url = response['image']
    # imgDownloadLock.release()
    return image_url




def getStepwiseRecipy(data, stepBreakdown='true'):
    '''
    Input:
        data: all previously preprocessed list of dictionaries
        stepBrealdown: whether to provide very detailed intructions
    output:
        data received from previous processed, added with {'steps': list}, {'image_url':url}

    '''

    # recipeLock.acquire()

    output = list()

    for raw in data:
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/%d/analyzedInstructions" % (
        raw['id'])

        querystring = {"stepBreakdown": stepBreakdown}
        headers = {
            'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
            'x-rapidapi-key': "4c32ba28bfmsheaba004aa4615a2p15a6cejsnb468180d57cd"
        }

        response = requests.request("GET", url, headers=headers, params=querystring, )

        response = response.json()

        if len(response) == 0:
            continue
        img_url=downloadImage(raw['id'])
        raw['image_url']=img_url
        raw['steps'] = [record['step'] for record in response[0]['steps']]
        output.append(raw)
    # recipeLock.release()
    return output





def processInput(ingredientsList):
    '''
    Input:
        ingredientsList: list of ingredients received from front-end
    Ouput:
        JSON file of format as list of dictionaries
         [ {'id':id,
            'title': titleRecipe,
            'ingredeints': list of ingredients,
            'image_url':url,
            'steps': list of sentences,
        }]
    '''
    # processLocker.acquire()
    # lemmaInp = [ingredient for ingredient in ingredientsList if len(ingredient.split(" ")) == 1]
    # nonLemmaInp = [ingredient for ingredient in ingredientsList if len(ingredient.split(" ")) > 1]

    # lemmaInp = ' '.join(lemmaInp)
    # ingredientsList = lemmatize(lemmaInp)
    # ingredientsList.extend(nonLemmaInp)



    recipes = recipesByIngredients(ingredientsList).json()

    processedRecipes = postProcess(recipes, ingredientsList)


    stepWiseRecipy = getStepwiseRecipy(processedRecipes)

    app.logger.info('[DEBUG] stepWiseRecipy: ')
    app.logger.info(stepWiseRecipy)
    #finalJson = json.dumps(stepWiseRecipy, separators=('\n', ":"), )
    # processLocker.release()
    return stepWiseRecipy
