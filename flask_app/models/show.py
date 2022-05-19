from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re
class Show:
    # initializing database name variable
    database_name = "tv_shows_"

    def __init__(self,data):
        self.id = data["id"]
        self.title = data["title"]
        self.network = data["network"]
        self.release_date = data["release_date"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None
        
    # this method saves a show in the database
    @classmethod
    def save_show(cls,data):
        query = "INSERT INTO shows (title,network,release_date,description,user_id) VALUES(%(title)s,%(network)s,%(release_date)s,%(description)s,%(id)s)" 
        connectToMySQL(Show.database_name).query_db(query,data)
        
    # this method get all shows from the database
    @classmethod
    def get_all_shows_with_users(cls):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id"
        shows = connectToMySQL(Show.database_name).query_db(query)
        shows_from_db = []
        # checking if we found any show
        if len(shows) == 0:
            return []
        else:
        # turning show results to objects
            for show in shows:
                # create a show object
                this_show = cls(show)
                # print(this_show)
                # create dict for user data
                this_user_dict = {
                    "id":show["users.id"],
                    "first_name":show["first_name"],
                    "last_name":show["last_name"],
                    "email":show["email"],
                    "password":show["password"],
                    "created_at":show["users.created_at"],
                    "updated_at":show["users.updated_at"]
                }
                # create a user instance
                this_user = user.User(this_user_dict)
                # link user to the show
                this_show.user = this_user
                shows_from_db.append(this_show)
            # returning list of show objects
            return shows_from_db
        
    # this method get one show from the database
    @classmethod
    def get_one_show_by_id(cls,data):
        query = "SELECT * FROM shows WHERE id = %(id)s"
        show = connectToMySQL(Show.database_name).query_db(query,data)
        # print(show)
        # checking if we found any show
        if len(show) == 0: 
            return None
        else:
            return cls(show[0])
        
    # this method edit show entry in the database
    @classmethod
    def update_show(cls,data):
        query = "UPDATE shows SET title = %(title)s,network = %(network)s,release_date = %(release_date)s,description = %(description)s WHERE id = %(id)s" 
        connectToMySQL(Show.database_name).query_db(query,data)
        
    #this method gets one show with its user from the database
    @classmethod
    def get_one_show_with_user(cls, data):
        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id WHERE shows.id = %(id)s;"
        show = connectToMySQL(Show.database_name).query_db(query, data)
        print(f"shows: {show}")
        # checking result has show
        if len(show) == 0:
            return None 
        else:
            # Create the show instance
            this_show = cls(show[0]) 
            #dictionary for the user data
            user_data = {
                "id":show[0]["users.id"],
                "first_name":show[0]["first_name"],
                "last_name":show[0]["last_name"],
                "email":show[0]["email"],
                "password":show[0]["password"],
                "created_at":show[0]["users.created_at"],
                "updated_at":show[0]["users.updated_at"]
            }
            # Creating a user instance
            this_user = user.User(user_data)
            # Link this user to this show
            this_show.user = this_user
            # Return the show - with the user linked
            return this_show
        
    # this method deletes show entry in the database
    @classmethod
    def delete_show(cls,data):
        query = "DELETE FROM shows WHERE id = %(id)s" 
        connectToMySQL(Show.database_name).query_db(query,data)
        
    # this method validates show inputs
    @staticmethod
    def validate_show_inputs(show):
        is_valid = True
        print(f"show: show")
        # regex to check for text input validity i.e title,network,description to be at least 3 characters
        text_regex = re.compile(r"^[a-zA-Z]{3,}")
        # checking if all fields are present
        if len(show['title']) == 0 or len(show['network']) == 0 or len(show['release_date']) == 0 or len(show['description']) == 0:
            flash("-All fields must be filled","input-error")
            is_valid = False
        if not (text_regex.match(show["title"])):
            # flash message and its category
            flash("-Title must be at least 3 characters","input-error")
            is_valid = False
        if not (text_regex.match(show["network"])):
            # flash message and its category
            flash("-Network must be at least 3 characters","input-error")
            is_valid = False
        if not (text_regex.match(show["description"])):
            # flash message and its category
            flash("-Description must be at least 3 characters","input-error")
            is_valid = False
        return is_valid
    
    
