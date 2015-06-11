import recipe
import pprint
import sys
import vegetarian
import cuisinetype
import Healthy as healthy

url = sys.argv[1]
a = recipe.recipe(url)
#pprint.pprint(a.getIngredients())
#pprint.pprint(a.getIngredients())
#pprint.pprint(a.getSteps())
#a = vegetarian.tovegetarian(a)
#print a.getCuisineType()
#pprint.pprint(a.getIngredients())
#a = healthy.tohealthy(a)
#pprint.pprint(a.getSteps())
#a = vegetarian.tovegetarian(a)
#pprint.pprint(a.getIngredients())
#print a.getCuisineType()
#pprint.pprint(a.getTools())
#print(a.getPrimaryMethod())
#a.getJSON()
#print a.getCuisineType()
recipe = cuisinetype.changetype(a, 'american')
pprint.pprint(recipe.ingredients)
pprint.pprint(recipe.steps)

