import bs4 as bs
import urllib2
import lists
import string
import nltk
import re
import nltk
import listcompiler
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math
import json
import operator

class recipe:
    learningMode = False
    ingredients = []
    steps = []
    tools = []
    originalSteps = []
    primarymethod = ""
    name = ''

    def __init__(self, url):
        ''' Constructor takes a URL from allrecipes.com and loads it.
            Returns recipe object '''
        self.url = url
        
        conn = urllib2.urlopen(url)
        self.html = conn.read()
        self.getName()
        self.initSteps()
        self.initIngredients()
        self.initTools()

    def resetRecipe(self):
        del self.ingredients[:]
        del self.steps[:]
        del self.tools[:]
        del self.originalSteps[:]
        self.primarymethod = ''
        self.name = ''

    def getName(self):
        soup = bs.BeautifulSoup(self.html)
        name = soup.find('h1', {'id': 'itemTitle'})
        self.name = name.string
        return self.name

    def getIngredients(self):
        if len(self.ingredients) == 0:
        	self.initIngredients()
        return self.ingredients

    def initIngredients(self):
        ''' getIngredients parses the ingredients from the page's HTML, then
            tries to find quantity, measurement, and descriptors
            INPUTS: recipe object
            OUTPUTS: dictionary of ingredients and their attributes '''
        del self.ingredients[:]
        soup = bs.BeautifulSoup(self.html)
        ingredients = soup('li', {'id': 'liIngredient'}) # find the ingredient list
        i = 0
        for ing in ingredients:
            self.ingredients.append({})
            try:
                amountStr = ing.find('span', {'class': 'ingredient-amount'}).string # the amount is in its own span
                amount = amountStr.split(" ")
                if '(' in amountStr and ')' in amountStr:
                    openingParen = amountStr.find('(')
                    closingParen = amountStr.find(')', openingParen)
                    self.ingredients[i]['descriptor'] = amountStr[openingParen+1:closingParen]
                    amountStr = amountStr[:openingParen-1] + amountStr[closingParen+1:]
                    amount = amountStr.split(' ')
                # split amount into quantity and measurement
                if len(amount) == 1:
                    self.ingredients[i]['quantity'] = amount[0]
                    self.ingredients[i]['measurement'] = ''
                elif len(amount) == 2:
                    self.ingredients[i]['quantity'] = amount[0]
                    self.ingredients[i]['measurement'] = amount[1]
                else:
                    if "/" in amount[1] and amount[0].isdigit():
                        self.ingredients[i]['quantity'] = float(amount[0])
                        vals = amount[1].split('/')
                        self.ingredients[i]['quantity'] += float(vals[0])/float(vals[1])
                        self.ingredients[i]['measurement'] = amount[2]
                    else: # not quite sure what would fall in this case, but gonna try it anyway
                        self.ingredients[i]['quantity'] = amount[0]
                        self.ingredients[i]['measurement'] = amount[1] + ' ' + amount[2]
                if self.ingredients[i]['measurement'] in lists.measurementAbbreviations.keys():
                    self.ingredients[i]['measurement'] = lists.measurementAbbreviations[self.ingredients[i]['measurement']]
                if (isinstance(self.ingredients[i]['quantity'], str) or isinstance(self.ingredients[i]['quantity'], unicode)) and not self.ingredients[i]['quantity'].isdigit(): 
                    if len(self.ingredients[i]['quantity'].split(' ')) == 2: # case of 1 1/2 type numbers
                        continue # filler until figured out what to do here
                    elif len(self.ingredients[i]['quantity'].split('-')) == 2: # case of 1-1/2 type numbers
                        continue # filler until figured out what to do here
                    elif len(self.ingredients[i]['quantity'].split('/')) == 2: # case of 1/2 type numbers
                        vals = self.ingredients[i]['quantity'].split('/')
                        self.ingredients[i]['quantity'] = float(vals[0])/float(vals[1])
                    else: # case where measurement is unmeasurable, like 'pinch' or 'to taste'
                        self.ingredients[i]['measurement'] = self.ingredients[i]['quantity'] + ' ' + self.ingredients[i]['measurement']
                        self.ingredients[i]['quantity'] = ''
                else:
                    self.ingredients[i]['quantity'] = float(self.ingredients[i]['quantity'])
            except AttributeError: # to taste is not considered a measurement by allrecipes.com, so we can get an error if there is no measurement. This exception catched that and tries to figure out a quantity
                name = ing.find('span', {'class': 'ingredient-name'}).string
                if 'to taste' in name: # if to taste is in the name, make the measurement to taste
                    self.ingredients[i]['measurement'] = 'to taste'
                    self.ingredients[i]['quantity'] = ''
            name = ing.find('span', {'class': 'ingredient-name'}).string # get ingredient name
            name2 = "".join(l for l in name if l not in string.punctuation)
            nameArr = name2.split(' ')
            descriptors = []
            preparers = []
            nameArr2 = []
            for word in nameArr:
                if word in lists.descriptors:
                    descriptors.append(word) # add the descriptor to descriptors
                elif word in lists.preparation:
                    if 'can' in self.ingredients[i]['measurement'] and word in ['diced', 'crushed']: # funky little thing to deal with canned crushed and diced things
                        nameArr2.append(word)
                    else:
                        preparers.append(word)
                else:
                    nameArr2.append(word)
            if 'descriptor' not in self.ingredients[i].keys():
                desc = '' # convert descriptors from array to string
                for j in range(len(descriptors)): # construct descriptors string from array
                    desc += descriptors[j] + ' '
                self.ingredients[i]['descriptor'] = desc.strip() # save descriptors
            prep = ''
            for j in range(len(preparers)): # construct preparation string from array
                prep += preparers[j] + ' '
            self.ingredients[i]['preparation'] = prep.strip() # save preparation
            name = ''
            if ('and' in nameArr2 and len(nameArr2)==2) or (len(nameArr2)==3 and 'and' in nameArr2 and nameArr2[1]!='and'):
                nameArr2.remove('and') # make sure there are no extraneous ands from the descriptors
            for j in range(len(nameArr2)): # construct name string from array
                name += nameArr2[j] + ' '
            if 'taste' in name: # deals with the case where ingredient is to taste
                pos = name.find('to taste')
                name = name[:pos] + name[pos+8:]
            self.ingredients[i]['name'] = name.strip() # save name
            i += 1
        return self.ingredients

    def getOriginalSteps(self):
        if len(self.originalSteps) == 0:
        	self.initOriginalSteps()
        return self.originalSteps

    def initOriginalSteps(self):
        ''' Parses the HTML for the recipe site and gets the recipe steps as defined there
            INPUTS: recipe object
            OUTPUTS: list of steps as defined in the recipe '''
        soup = bs.BeautifulSoup(self.html)
        directions = soup.find('div', {'class': 'directions'}) # tries to find the area directions are in
        directions = directions.find('ol') # the steps are in an ordered list
        sitesteps = directions('li') # each step is its own list item
        steps = []
        for step in sitesteps:
            steps.append(step.find('span').string) # append the string (the step) to the steps list
        i = 0
        self.originalSteps = steps
        return self.originalSteps

    def getSteps(self):
        if len(self.steps) == 0:
        	self.initSteps(self)
        return self.steps

    def initSteps(self):
        ''' Parses the HTML for the recipe site and gets the recipe steps as defined there
            INPUTS: recipe object
            OUTPUTS: list of steps'''
        if len(self.originalSteps) == 0:
            self.getOriginalSteps()
        if len(self.tools) == 0:
            self.getTools()
        if len(self.ingredients) == 0:
            self.getIngredients()

        i = 0
        dontClear = False
        for step in self.originalSteps:
            sentences = step.split('.')
            for sentence in sentences:
                if sentence == '':
                    continue
                if dontClear != True:
                    self.steps.append({})
                    self.steps[i]['tools'] = []
                    self.steps[i]['ingredients'] = []
                    self.steps[i]['action'] = []
                dontClear = False
                words = sentence.split()
                time = ''
                for j in range(len(words)):
                    word = words[j]
                    word = word.lower()
                    if word in lists.tools or word in self.tools:
                        self.steps[i]['tools'].append(word)
                    for ingredient in self.ingredients:
                        if word in ingredient['name'].split():
                            self.steps[i]['ingredients'].append(ingredient['name'])
                    if word in lists.assumedIngredients:
                        self.steps[i]['ingredients'].append(word)
                    if word in lists.actions:
                        self.steps[i]['action'].append(word)
                    if word in lists.time:
                        if j>=2 and words[j-2]=='to':
                            time += words[j-3] + ' to ' + words[j-1] + ' ' + word + ' '
                        else:
                            time += words[j-1] + ' ' + word + ' '
                    if word == "until":
                        if j+1 < len(words):
                            time += 'until ' + words[j+1] + ' '

                self.steps[i]['ingredients'] = list(set(self.steps[i]['ingredients']))
                self.steps[i]['time'] = time.strip()
                if len(self.steps[i]['ingredients']) == 0 and i>0:
                    self.steps[i]['ingredients'] = self.steps[i-1]['ingredients'] # probably the previous list of ingredients applies still
                if len(self.steps[i]['tools']) == 0 and i>0:
                    self.steps[i]['tools'] = self.steps[i-1]['tools'] # probably the previous tools apply here
                if len(self.steps[i]['ingredients']) == 0 and i==0:
                    dontClear = True
                    continue # probably a silly instruction that we can't figure out, so just leave it out and hope the next step helps
                if ('stir' in self.steps[i]['action'] or 'simmer' in self.steps[i]['action']) and i > 0:
                	self.steps[i]['ingredients'].extend(self.steps[i-1]['ingredients'])
                	self.steps[i]['ingredients'] = list(set(self.steps[i]['ingredients']))
                if len(self.steps[i]['action']) != 0: # if there is an action, advance to the next step; if there's no action, let's ignore this step and try the next sentence
                    i += 1
        i = 0
        while i < len(self.steps):
            step = self.steps[i]
            if len(step) == 0:
                self.steps.remove(step)
            else:
                i += 1
        return self.steps # return the steps, which are also saved in the object

    def getPrimaryMethod(self):
        if self.primarymethod == "":
        	self.initPrimaryMethod()
        return self.primarymethod

    def initPrimaryMethod(self):
        ''' Uses rudimentary method to determine the primary cooking method and returns it.
            INPUTS: recipe object
            OUTPUTS: string containing primary cooking method'''
        if len(self.originalSteps) == 0: # if we don't already have the steps loaded, get them
            self.getOriginalSteps()
        for i in reversed(range(len(self.originalSteps))): # starting from the last step
            for method in lists.primaryCookingMethods: # look for a primary cooking method
                if method in self.originalSteps[i].lower():
                    self.primarymethod = method
                    return method # if one is found, return it
        if "stir" in self.name.lower():
            self.primarymethod = "Stir-Fry"
            return "Stir-Fry"
        return None # if none is found, don't return anything

    def getTools(self):
        if len(self.tools) == 0:
        	self.initTools()
        self.tools = list(set(self.tools))
        return self.tools

    def initTools(self):
        ''' Reads through the steps and finds tool words in them. Creates a list of the tools
            mentioned in the steps
            INPUTS: recipe object
            OUTPUTS: list of tools'''
        if len(self.originalSteps) == 0:
            self.getOriginalSteps()
        for s in self.originalSteps:
            tokens = nltk.word_tokenize(s) # tokenize the steps into words
            bigram = bigrams(tokens) # and bigrams too, since some tools are two words
            for t in tokens: # now making list of tools
                t = t.strip().lower()
                if t in lists.tools:
                    self.tools.append(t)
                if t in lists.impliedTools.keys():
                    self.tools.append(lists.impliedTools[t])
            for t in bigram:
                t = t[0].strip().lower() + " " + t[1].strip().lower()
                if t in lists.tools:
                    self.tools.append(t)
            # This section is for making the program able to add previously unseen ingredients to its growing library
            for x in range(len(tokens)):
                if (tokens[x] == "a"):
                    add = (tokens[x+1:x+4])
                    add = bigrams(add)
                    for t in add:
                        t = t[0] + " " + t[1]
                        t = t.strip().lower()
                        t = RePunc(t)
                        new = 0
                        for j in listcompiler.equipment:
                            if t == j:
                                new = 1
                                self.tools.append(t)
                        if new == 0 and self.learningMode:
                             print "Unrecognized input: ", t
                             Answer = raw_input("Should this be added to the universal equipment bank (Y/N)? \n")
                             if (Answer == 'y' or Answer == 'Y' ):
                                 listcompiler.addtolist('lists/equipment.csv', t)
                                 self.tools.append(t)
        self.tools = list(set(self.tools))
        return self.tools # return list of tools

    def getCuisineType (self):
        #vote on cusine by looking at how ingredients fall under a particular cuisine
        ethnicity = {"american":0, "italian":0, "asian":0, "mexican":0}

        if len(self.ingredients) == 0:
            self.getIngredients()

        for ingredient in self.ingredients:
            for word in lists.american:
                if word.lower() in ingredient["name"].lower():
                    #print 'american'
                    ethnicity["american"] += 1
            for word in lists.italian:
                if word.lower() in ingredient["name"].lower():
                    #print 'italian'
                    ethnicity["italian"] += 1
            for word in lists.asian:
                if word.lower() in ingredient["name"].lower():
                    #print 'asian'
                    ethnicity["asian"] += 1
            for word in lists.mexican:
                if word.lower() in ingredient["name"].lower():
                    #print 'mexican'
                    ethnicity["mexican"] += 1
            if 'curry' in ingredient['name'].lower():
            	return 'asian'

        return max(ethnicity.iteritems(), key=operator.itemgetter(1))[0]

    def swapStepIngredients(self, original, new):
        for i in range(len(self.steps)):
            step = self.steps[i]
            for j in range(len(step['ingredients'])):
                ingredient = step['ingredients'][j]
                if ingredient == original:
                    self.steps[i]['ingredients'][j] = new
        return self.steps
    
    def swapStepMethod(self, original, new):
        for i in range(len(self.steps)):
            step = self.steps[i]
            for j in range(len(step['action'])):
                action = step['action'][j]
                if action == original:
                    self.steps[i]['action'][j] = new
        return self.steps
    
    def printIngredients(self):
        print "INGREDIENTS:"
        template = "{name:30}|{quantity:8}|{measurement:15}|{descriptor:30}|{preparation:30}"
        print template.format(name='Ingredient', quantity='Quantity', measurement='Measurement', descriptor='Descriptor', preparation='Preparation')
        for rec in self.ingredients: 
              print template.format(**rec)

    def printSteps(self):
        print "STEPS:"
        template = "{action:20}|{ingredients:75}|{tools:30}|{time:20}"
        print template.format(action="Action(s)", ingredients="Ingredients", tools="Tools", time="Time")
        for rec in self.steps:
            act = ''
            ing = ''
            too = ''
            for action in rec['action']:
                act += action + ', '
            act = act[:-2]
            for ingredient in rec['ingredients']:
                ing += ingredient + ', '
            ing=ing[:-2]
            for tool in rec['tools']:
                too += tool + ', '
            too = too[:-2]

            print template.format(action=act, ingredients=ing, tools=too, time=rec['time'])

    def printTools(self):
        for tool in self.tools:
            print tool

    def getJSON(self):
        ret = {'ingredients': self.getIngredients(), 'cooking method': self.getPrimaryMethod(), 'cooking tools': self.getTools()}
        ret = json.dumps(ret)
        print ret
        return ret

def RePunc(strang):
    words =str(strang)
    words = words.translate(None, ',')
    words = words.translate(None, '"')
    words = words.translate(None, '.')
    words = words.translate(None, '...')
    words = words.translate(None, '?')
    words = words.translate(None, '!')
    words = words.translate(None, ';')
    words = words.translate(None, '-')
    words = words.translate(None, '\'')
    words = words.translate(None, '.\'')
    words = words.translate(None, '(')
    words = words.translate(None, ')')
    words = words.translate(None, ':')
    return(words)

