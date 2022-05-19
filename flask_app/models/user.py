from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
class User:
    # initializing database name variable
    database_name = "tv_shows_"

    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.shows = []
        
    # this method creates user entry in the database
    @classmethod
    def register_user(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)" 
        # retrieving the id of created user for session
        user_id = connectToMySQL(User.database_name).query_db(query,data)
        return user_id
    
    # this method verifies users
    @classmethod
    def verify_user(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        user = connectToMySQL(User.database_name).query_db(query,data)
        # checking if we found any user
        if len(user) == 0:
            return False
        else:
            return cls(user[0])
        
    # this method get one user from the database
    @classmethod
    def get_one_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user = connectToMySQL(User.database_name).query_db(query,data)
        # checking if we found any user
        if len(user) == 0:
            return None
        else:
            return cls(user[0])
        
    # this method flashed error messages after validating user inputs
    @staticmethod
    def user_validation(user):
        is_valid = True
        # regex to check for names validity
        name_regex = re.compile(r"^[a-zA-Z]{3,}")
        # regex to check for email validity
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # regex for password validity 
        password_regex = re.compile(r"^[a-zA-Z0-9]{8,}")
        # checking if all fields are present
        if len(user['first_name']) == 0 or len(user['last_name']) == 0 or len(user['email']) == 0 or len(user['password']) == 0 or len(user['confirmed_password']) == 0:
            flash("-All fields must be filled","register-error")
            is_valid = False
        # checking if First Name - characters only, at least 3 characters
        if not (name_regex.match(user["first_name"])) :
            flash("- First name must be at least 3 characters","register-error")
            is_valid = False
        # checking if Last Name - characters only, at least 3 characters
        if not (name_regex.match(user["last_name"])):
            # flash message and its category
            flash("- Last name must be at least 3 characters","register-error")
            is_valid = False
        # checking for email format validity
        if not email_regex.match(user["email"]):
            # flash message and its category
            flash("- Please enter a valid email address example:name@example.com","register-error")
            is_valid = False
        # checking for password min 8 characters
        if not password_regex.match(user["password"]):
            # flash message and its category
            flash("- Password must be at least 8 characters","register-error")
            is_valid = False
        # checking for match btn password and password confirmation field
        if not user["password"] == user["confirmed_password"]:
            # flash message and its category
            flash("- Entered password must be the same as confirmed password","register-error")
            is_valid = False
        return is_valid
    
    # this method flashes error messages only when invalid credentials have been entered
    @staticmethod
    def user_login_validation(user):
        is_valid = True
        # regex for password validity 
        login_password_regex = re.compile(r"^[a-zA-Z0-9]{8,}")
        # regex to check for email validity
        email_regex = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # checking if all fields are present
        if len(user['email']) == 0 or len(user['password']) == 0:
            flash("-All fields must be filled","login-error")
            is_valid = False
        # check for valid email
        if not email_regex.match(user["email"]):
            flash("- Please enter a valid email address example:name@example.com","login-error")
            is_valid = False
        # checking for password min 8 characters
        if not login_password_regex.match(user["password"]):
            # flash message and its category
            flash("- Password must be at least 8 characters","login-error")
            is_valid = False
        return is_valid
    
    # this method flash error message for incorrect credentials
    @staticmethod
    def get_error_message():
        # below statement will be flashed when credentials are not correct
        flash("- Invalid Credentials","login-error")
