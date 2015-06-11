import recipe
import lists

#main function
def changetype (recipe, desiredType):
    recipe, removelist = getCuisineSpecificIngredients(recipe)
    if desiredType == 'american':
        recipe = toAmerican(recipe, removelist)
    elif desiredType == 'asian':
        recipe = toAsian(recipe, removelist)
    elif desiredType == 'mexican':
        recipe = toMexican(recipe, removelist)
    elif desiredType == 'italian':
        recipe = toItalian(recipe, removelist)
    return recipe
    


#a function that pulls out cuisine specific ingredients
def getCuisineSpecificIngredients (recipe):
    cuisinetype = recipe.getCuisineType()

    if cuisinetype == "american":
        inglist = lists.american
    elif cuisinetype == "asian":
        inglist = lists.asian
    elif cuisinetype == "italian":
        inglist = lists.italian
    elif cuisinetype == "mexican":
        inglist = lists.mexican

    removelist = []

    for ingredient in recipe.ingredients:
        for item in inglist:
            if item.lower().strip() in ingredient['name'].lower().strip():
                removelist.append(ingredient)
                break

    for ingredient in removelist:
        recipe.ingredients.remove(ingredient)

    return (recipe, removelist)


#a funtion to convert TO AMERICAN
def toAmerican (recipe, removelist):
    for ingredient in removelist:
        for item in lists.equivalencies:
            if item["asian"].lower() in ingredient["name"].lower():
                if item['asian'] == '':
                    continue
                #print "Replacing " + ingredient['name'] + ' with ' + item['american']
                recipe.ingredients.append({"name":item["american"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['american'])
                break
            elif item["italian"].lower() in ingredient["name"].lower():
                if item['italian'] == '':
                    continue
                #print "Replacing " + ingredient['name'] + ' with ' + item['american']
                recipe.ingredients.append({"name":item["american"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['american'])
                break
            elif item["mexican"].lower() in ingredient["name"].lower():
                if item['mexican'] == '':
                    continue
                #print "Replacing " + ingredient['name'] + ' with ' + item['american']
                recipe.ingredients.append({"name":item["american"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['american'])
                break

    return recipe
                
#a function to convert TO ASIAN
def toAsian (recipe, removelist):
    for ingredient in removelist:
        for item in lists.equivalencies:
            if item["american"].lower() in ingredient["name"].lower():
                if item['american'] == '':
                    continue
                recipe.ingredients.append({"name":item["asian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['asian'])
                break
            if item["italian"].lower() in ingredient["name"].lower():
                if item['italian'] == '':
                    continue
                recipe.ingredients.append({"name":item["asian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['asian'])
                break
            if item["mexican"].lower() in ingredient["name"].lower():
                if item['mexican'] == '':
                    continue
                recipe.ingredients.append({"name":item["asian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['asian'])
                break

    return recipe
                


#a function to convert TO ITALIAN
def toItalian (recipe, removelist):
    for ingredient in removelist:
        for item in lists.equivalencies:
            if item["asian"].lower() in ingredient["name"].lower():
                if item['asian'] == '':
                    continue
                recipe.ingredients.append({"name":item["italian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['italian'])
                break
            if item["american"].lower() in ingredient["name"].lower():
                if item['american'] == '':
                    continue
                recipe.ingredients.append({"name":item["italian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['italian'])
                break
            if item["mexican"].lower() in ingredient["name"].lower():
                if item['mexican'] == '':
                    continue
                recipe.ingredients.append({"name":item["italian"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['italian'])
                break

    return recipe


#a function to conver TO MEXICAN
def toMexican (recipe, removelist):
    for ingredient in removelist:
        for item in lists.equivalencies:
            if item["american"].lower() in ingredient["name"].lower():
                if item['american'] == '':
                    continue
                recipe.ingredients.append({"name":item["mexican"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['mexican'])
                break
            if item["italian"].lower() in ingredient["name"].lower():
                if item['italian'] == '':
                    continue
                recipe.ingredients.append({"name":item["mexican"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['mexican'])
                break
            if item["asian"].lower() in ingredient["name"].lower():
                if item['asian'] == '':
                    continue
                recipe.ingredients.append({"name":item["mexican"], "descriptor": '', "measurement": ingredient['measurement'], 'preparation': ingredient['preparation'], 'quantity': ingredient['quantity']})
                recipe.swapStepIngredients(ingredient['name'], item['mexican'])
                break

    return recipe


