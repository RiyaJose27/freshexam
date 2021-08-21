import re
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/recipes')
def exam_index():
    if 'user_id' not in session:
        flash('Please log in to view this page')
        return redirect('/')
    recipes = Recipe.get_all_recipes()
    print(recipes)
    
    return render_template('recipes.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    return render_template('new_recipe.html')


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    
    if Recipe.validate_recipe(request.form):
        data = {
            'name' : request.form['name'],
            'date' : request.form['date'],
            'description' : request.form['description'],
            'instruction' : request.form['instruction'],
            'minutes'  : request.form['minutes'],
            'users_id' : session['user_id']
        }
        Recipe.create_recipe(data)
        print('recipe valid')
        return redirect('/recipes')
    print('recipe not valid')
    
    return redirect('/recipes/new')


@app.route('/recipes/<int:recipe_id>')
def recipe_info(recipe_id):
    
    recipe = Recipe.get_recipe_by_id({'id' : recipe_id})
    
    return render_template('recipe_info.html', recipe = recipe)
    
    
@app.route('/info/recipes/')
def info_recipe():
    recipes = Recipe.get_all_recipes()
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    
    recipe = Recipe.get_recipe_by_id({'id' : recipe_id})
    
    # if session['user_id'] != recipe.users_id:
    #     return redirect(f'/recipes/{recipe_id}')
    
    return render_template('edit_show.html', recipe = recipe)


@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    if Recipe.validate_recipe(request.form):
        data = {
            'name' : request.form['name'],
            'date' : request.form['date'],
            'description' : request.form['description'],
            'instruction' : request.form['instruction'],         
            'id' : recipe_id
        }
        Recipe.update_recipe(data)
        
    return redirect(f'/recipes/{recipe_id}/edit')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe = Recipe.get_recipe_by_id({'id' : recipe_id})
    
    if session['user_id'] != recipe.users_id:
        return redirect(f'/recipes/{recipe_id}')
    
    return render_template('delete_show.html', recipe = recipe)
    
@app.route('/recipes/<int:recipe_id>/confirm')
def confirm_delete_recipe(recipe_id):
    Recipe.delete_recipe({'id' : recipe_id})
    
    return redirect('/recipes')