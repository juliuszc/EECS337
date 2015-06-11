import recipe
import pprint
import sys
import vegetarian
import cuisinetype
import Healthy as healthy

url = sys.argv[1]
a = recipe.recipe(url)
a.getJSON()

