import recipe
import lists

def tovegetarian(recipe):
	#identify protein (to remove or substitute)
	meats = []
	for ingredient in recipe.ingredients:
		for meat in lists.proteins:
			if meat in ingredient["name"]:
				meats.append(ingredient)
				break
	# remove meat from recipe
	for meat in meats:
		recipe.ingredients.remove(meat)


	type = recipe.getCuisineType()

	for meat in meats:
	    liquid = False
	    for liquid in lists.liquids:
	    	if liquid in meat['name'].lower():
	    	    #print "Liquid found!"
	    	    liquid = True
	    	    break
	    if liquid == True:
	    	#print "Liquid substitution"
	    	recipe.ingredients.append({'name': 'vegetable broth', 'descriptor': '', 'measurement': meat['measurement'], 'quantity': meat['quantity'], 'preparation': ''})
	    	recipe.swapStepIngredients(meat['name'], 'vegetable broth')
	    elif type == "american":
		    recipe.ingredients.append({'name':'mushroom', 'descriptor': '', 'measurement': meat['measurement'], 'quantity': meat['quantity'], 'preparation': meat['preparation']})
		    recipe.swapStepIngredients(meat['name'], 'mushroom')
	    elif type == "italian":
		    recipe.ingredients.append({'name':'eggplant', 'descriptor': '', 'measurement': meat['measurement'], 'quantity': meat['quantity'], 'preparation': meat['preparation']})
		    recipe.swapStepIngredients(meat['name'], 'eggplant')
	    elif type == "asian":
		    recipe.ingredients.append({'name':'tofu', 'descriptor': '', 'measurement': meat['measurement'], 'quantity': meat['quantity'], 'preparation': meat['preparation']})
		    recipe.swapStepIngredients(meat['name'], 'tofu')
	    elif type == "mexican":
		    recipe.ingredients.append({'name':'peppers', 'descriptor': '', 'measurement': meat['measurement'], 'quantity': meat['quantity'], 'preparation': 'chopped'})
		    recipe.swapStepIngredients(meat['name'], 'peppers')

	return recipe





