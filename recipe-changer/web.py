import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import os
import recipe as recipeClass
import vegetarian
import cuisinetype
import Healthy as healthy
import copy

app=Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def promptUser():
    return render_template('promptUser.html')

@app.route('/originalRecipe', methods=['GET','POST'])
def getOriginalRecipe():
    url = request.form['url']
    try:
        recipe = recipeClass.recipe(url)
        recipe.resetRecipe()
    except:
        return render_template('promptUser.html', error='This other error')
    try:
        recipe = recipeClass.recipe(request.form['url'])
    except:
        return render_template('promptUser.html', error='There was a problem with the recipe you entered. Either the recipe was not from allrecipes.com, or there was a malformed expression within the recipe.')
    return render_template('displayRecipe.html', url=request.form['url'], recipe=recipe, transform='', error='')

@app.route('/transform', methods=['GET', 'POST'])
def transformRecipe():
    url = request.form['url']
    transformation = request.form['transformation']
    try:
        recipe = recipeClass.recipe(url)
        recipe.resetRecipe()
    except:
        return render_template('promptUser.html', error='This error')
        pass
    try:
        recipe = recipeClass.recipe(url)
    except:
        return render_template('promptUser.html', error='There was a problem retrieving the original recipe. Your internet connection may be down.')
    try:
        if transformation=='vegetarian':
            recipe = vegetarian.tovegetarian(recipe)
        elif transformation=='healthy':
            recipe = healthy.tohealthy(recipe)
        elif transformation=='american' or transformation=='mexican' or transformation=='italian' or transformation=='asian':
            recipe = cuisinetype.changetype(recipe, transformation)
        else:
        	return render_template('displayRecipe.html', url=url, recipe=recipe, transform='', error='There was a problem transforming your recipe. The original recipe is displayed below.')
    except:
        return render_template('displayRecipe.html', url=url, recipe=recipe, transform='', error='There was a problem transforming your recipe. The original recipe is displayed below.')
    return render_template('displayRecipe.html', url=url, recipe=recipe, transform=transformation, error='')

@app.route('/transformations')
def aboutTransformations():
    return render_template('transformations.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
	    app.run()

