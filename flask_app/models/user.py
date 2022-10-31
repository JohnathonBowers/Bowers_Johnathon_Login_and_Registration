from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

NAME_REGEX = re.compile('\d')

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
        if EMAIL_REGEX.match(user['email']):
            flash('Please enter a valid email address', 'email')
            is_valid = False

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL('login_registration_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])