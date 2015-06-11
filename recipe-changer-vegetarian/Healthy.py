#!/usr/bin/env python


import recipe
import lists

def tohealthy(recipe):
        #change cooking method to healthy alternative
        for i in range(len(recipe.steps)):
            method = recipe.steps[i]
            for methods in lists.healthy:
                if methods in method["action"]:
                    recipe.steps[i]["action"] = [lists.healthy[methods]]
                    recipe.steps[i]["tools"] = ["baking pan"]
                    break
        
	#identify protein (to remove or substitute)
	for i in range(len(recipe.ingredients)):
            ingredient = recipe.ingredients[i]
	    for ingredients in lists.healthy:
		if ingredients in ingredient["name"]:
		    recipe.ingredients[i]["name"] = lists.healthy[ingredients]
		    break



	return recipe

