# Recipely Backend API

This is the back-end for the [Recipely app](https://github.com/JinhaJjing/CodeSpillers) that Team Code Spillers developed during JunctionX Seoul 2020. 

Team Code Spillers was: Eve, Farrukh Olimov, JinHa Suh, Seung Hyun Lee, [Shikha Dubey](https://github.com/shikha-gist/), Victor Gonzalez Prieto.

The server is no longer running but you can find a short demo of the app [here](https://www.youtube.com/watch?v=RfBj1pXpNwo&feature=youtu.be).

---

Recipely is an app for finding recipes based on a set of ingredients you have in your fridge and feel like eating.

Example request:

```shell
curl -X POST "https://agile-sands-61557.herokuapp.com/application/recipes/" -H "accept: application/json"t-Type: application/json" -d "{ \"ingredients\" : [ \"apples\", \"bananas\", \"mango\", \"milk\", \"ginger\", \"meat\", \"eggs\", \"water\", \"caramels\", \"juice\", \"spinach\", \"flour\", \"tomatoes\", \"onion\"]}"
```

Example response:

```
{"recipes":[{"id":987595,"image_url":"https://spoonacular.com/recipeImages/987595-556x370.jpg","ingredients":["apple","ginger"],"nutritions":{"calories":"96","carbs":"23g","fat":"0.61g","protein":"1g"},"steps":["Combine ingredients in a glass and stir to mix.","Garnish with thinly sliced apples if desired."],"title":"Apple Ginger Kombucha Cocktail","video_url":"none"},{"id":66531,"image_url":"https://spoonacular.com/recipeImages/66531-556x370.jpg","ingredients":["apple","sweetened condensed milk"],"nutritions":{"calories":"313","carbs":"58g","fat":"7g","protein":"5g"},"steps":["Place caramels in a 3-quart slow cooker; stir in condensed milk.","Cover and cook on LOW 3 1/2 hours, stirring occasionally, until caramels melt and mixture is smooth.","Serve with apple slices and pound cake squares.","Party Plan: Keep this fondue warm in the slow cooker for easy dipping. Reheat any leftovers in the microwave, stirring at 1-minute intervals until heated through."],"title":"Caramel Fondue","video_url":"youtube.com/watch?v=sROO2mtz7uQ"}]}
```
