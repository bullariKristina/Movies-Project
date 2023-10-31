from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    db_name = 'movies_db'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.profile_pic = data['profile_pic']
        self.email = data['email']
        self.passowrd = data['password']
        self.verification_code = data['verification_code']
        self.is_verified = data['is_verified']
        self.admin = data['admin']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_last_user(cls):
        query = 'SELECT * FROM users ORDER BY created_at DESC LIMIT 1;'
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return results[0]
        return False
    

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, verification_code, is_verified, admin) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(verification_code)s, %(is_verified)s, %(admin)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def add_profile_pic(cls,data):
        query = "UPDATE users SET profile_pic = %(profile_pic)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getlastuser(cls):
        query = 'SELECT * FROM users ORDER BY created_at DESC LIMIT 1;'
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return results[0]
        return False
    
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE users SET is_verified = 1 WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE users SET verification_code = %(verification_code)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
   
    #All information of all users
    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users= []
        if results:
            for user in results:
                users.append(user)
            return users
        return users

    
    @classmethod
    def get_id(cls, data):
        query = "SELECT id FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results['id']
        return False

    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_movies(cls, data):
        query = "SELECT * FROM movies JOIN users ON users.id = movies.user_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def comment(cls):
        query = "INSERT INTO comments (comment, movie_id, user_id) VALUES (%(comment)s, %(movie_id)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'confirmPassword')
            is_valid = False
        return is_valid
    

    #It valides when user tries to update 
    @staticmethod
    def validate_user_on_update(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 2:
           flash('First name must be more than 2 characters', 'firstName')
           is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False 
        else:
            flash('User updated successfully!!', 'successfullUpdate')    
        return is_valid
    