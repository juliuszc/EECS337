import recipe
import pprint
import sys
import vegetarian
import cuisinetype
import Healthy as healthy

url = sys.argv[1]
a = recipe.recipe(url)
print "RECIPE NAME:"
print a.getName()
print "PRIMARY COOKING METHOD:"
print a.getPrimaryMethod()
print "\n\n"
a.printIngredients()
print "\n\n"
a.printSteps()
print "\n\nTOOLS:"
a.printTools()
print "\n\n\n"
print "TRANSFORMATIONS:\n1. Vegetarian\n2. Healthy\n3. American Cuisine\n4. Asian Cuisine\n5. Italian Cuisine\n6. Mexican Cuisine\n0. Exit without Transformation"
while(True):
    selection = int(raw_input("Please select transformation: "))
    if selection in [1, 2, 3, 4, 5, 6, 0]:
        break
    else:
        print "Invalid selection!"
if selection == 1:
    newRecipe = vegetarian.tovegetarian(a)
elif selection == 2:
    newRecipe = healthy.tohealthy(a)
elif selection == 3:
    newRecipe = cuisinetype.changetype(a, 'american')
elif selection == 4:
    newRecipe = cuisinetype.changetype(a, 'asian')
elif selection == 5:
    newRecipe = cuisinetype.changetype(a, 'italian')
elif selection == 6:
    newRecipe = cuisinetype.changetype(a, 'mexican')
if selection in [1, 2, 3, 4, 5, 6]:
    # because of a python design decision newRecipe = a. I forgot about that until I made the below mistake, and just am not bothering to change it.
    print "TRANSFORMATION OF RECIPE:"
    print a.getName()
    print "PRIMARY COOKING METHOD:"
    print a.getPrimaryMethod()
    print "\n\n"
    a.printIngredients()
    print "\n\n"
    a.printSteps()
    print "\n\nTOOLS:"
    a.printTools()

