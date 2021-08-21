from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re

class User():
    
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
        
        
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(email)s, %(password)s,NOW(),NOW());"
        
        result = connectToMySQL('exam_schema').query_db(query, data)
        
        return result
        
    @classmethod
    def get_users_with_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s; "
        
        results = connectToMySQL('exam_schema').query_db(query, data)
        
        users = []
        
        for item in results:
            users.append(User(item))
            
        return users 
    

    
    @classmethod
    def get_users_with_first_name(cls, data):
        query = "SELECT * FROM users WHERE first_name = %(first_name)s;"
        
        results = connectToMySQL('exam_schema').query_db(query, data)
        
        users = []
        
        for item in results:
            users.append(User(item))
            
        return users 

        
        
    
    @staticmethod
    def validate_registration(data):
    
        is_valid = True
        
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            
        if len(data['first_name']) < 2 or len(data['first_name']) > 32:
            flash("Firstname should be 2 to 32 characters")
            is_valid = False
            
        if not email_regex.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
            
        if len(data['password']) < 8:
            flash("Please use a password of at least eight characters")
            is_valid = False
            
        if data['password'] != data['confirm_password']:
            flash("Please insure password and confirm password match")
            is_valid = False
            
        if len(User.get_users_with_email({'email' : data['email']})) != 0:
            flash("This email address is already in use.")
            is_valid = False
    
        if len(User.get_users_with_first_name({'first_name' : data['first_name']})) != 0:
            flash("This firstname is already in use.")
            is_valid = False
            
        
        return is_valid