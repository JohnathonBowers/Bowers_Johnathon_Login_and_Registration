from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# I adapted the name regex from part of the password regex below
NAME_REGEX = re.compile('(?=.*?[0-9])')

# I referred to uibakery.io for how to construct this password regex
PWD_REGEX = re.compile('^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[!@#$%^&*-?]).{8,20}$')

class User:
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must include two or more characters', 'first_name')
            is_valid = False
        if NAME_REGEX.match(user['first_name']):
            flash('First name must not include numbers', 'first_name')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must include two or more characters', 'last_name')
            is_valid = False
        if NAME_REGEX.match(user['last_name']):
            flash('Last name must not include numbers', 'last_name')
            is_valid = False
        if len(user['email']) < 1:
            flash('Email address required', 'email')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Please enter a valid email address', 'email')
            is_valid = False
        if not PWD_REGEX.match(user['password']):
            flash('Please enter a password that meets the required criteria', 'password')
            is_valid = False
        if (user['confirm_password']) != (user['password']):
            flash('Passwords do not match!', 'confirm_password')
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('login_registration_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL('login_registration_schema').query_db(query, data)
    
    @classmethod
    def get_by_user_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('login_registration_schema').query_db(query, data)
        return cls(result[0])