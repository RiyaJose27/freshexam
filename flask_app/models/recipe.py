from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL


from flask_app.models.user import User
class Recipe():
    
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.description= data['description']
        self.instruction = data['instruction']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.minutes = data['minutes']
        self.users_id = data['users_id']
        self.user = None
        
        
        
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, date, description, instruction, created_at, updated_at, minutes, users_id) VALUES (%(name)s,%(date)s, %(description)s, %(instruction)s,NOW(),NOW(), %(minutes)s,%(users_id)s);"
        
        result = connectToMySQL('exam_schema').query_db(query, data)
        
        
    @classmethod
    def get_all_recipes(cls):
        query = 'SELECT * FROM recipes JOIN users ON recipes.users_id = users.id;'
    
        results = connectToMySQL ('exam_schema').query_db(query)
        
        recipes = []
        
        for item in results:
            recipe = cls(item)
            user_data = {
                'id' : item['users_id'],
                'first_name' : item['first_name'],
                'email' : item ['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item ['users.updated_at']
            }
            recipe.user = User(user_data)  
            recipes.append(recipe)
        return recipes
    
    
    @classmethod
    def get_recipe_by_id(cls, data):
        query = 'SELECT * FROM recipes JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s;'
        
        result = connectToMySQL('exam_schema').query_db(query, data)
        
        recipe = cls(result[0])
        user_data = {
            'id' : result[0]['users_id'],
            'first_name' : result[0]['first_name'],
            'email' : result[0]['email'],
            'password' : result[0]['password'],
            'created_at' : result[0]['users.created_at'],
            'updated_at' : result[0]['users.updated_at']
        }
        recipe.user = User(user_data)
        return recipe
        
    @classmethod
    def update_recipe(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, date = %(date)s  WHERE id = %(id)s;'
        
        connectToMySQL('exam_schema').query_db(query, data)
        
    @classmethod
    def delete_recipe(cls, data):
    
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL('exam_schema').query_db(query, data)
        
    @staticmethod
    def validate_recipe(data):
    
        is_valid = True
        
        if len(data['name']) < 3:
            flash("Firstname should be 3 to 32 characters")
            is_valid = False
            
            
        if len(data['description']) < 3:
            flash("Description should be 3 to 32 characters")
            is_valid = False
        
        if len(data['instruction']) < 3:
            flash("Instruction should be 3 to 32 characters")
            is_valid = False
        
        return is_valid
    