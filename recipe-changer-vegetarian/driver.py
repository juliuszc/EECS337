import recipe
import pprint

a = recipe.recipe('http://allrecipes.com/Recipe/Blackened-Chicken/Detail.aspx?soid=recs_recipe_4')
pprint.pprint(a.getIngredients())
pprint.pprint(a.getSteps())
pprint.pprint(a.getTools())
print(a.getPrimaryMethod())
#a.getJSON()
