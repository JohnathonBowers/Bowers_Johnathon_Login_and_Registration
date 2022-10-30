from flask_app.config.mysqlconnection import connectToMySQL

class User:
    def __init__ (self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    