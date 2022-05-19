from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
class Like:
    # initializing database name variable
    database_name = "tv_shows_"

    def __init__(self,data):
        self.id = data["id"]
        self.count = data["count"]
        self.user_id = data["user_id"]
        self.show_id = data["show_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    # this method saves a like in the database
    @classmethod
    def save_like(cls,data):
        query = "INSERT INTO likes (count,user_id,show_id) VALUES(%(count)s,%(user_id)s,%(show_id)s)" 
        connectToMySQL(Like.database_name).query_db(query,data)
        
    # this method like from the database by show id
    @classmethod
    def get_likes_by_show_id(cls,data):
        query = "SELECT * FROM likes WHERE show_id = %(id)s"
        like = connectToMySQL(Like.database_name).query_db(query,data)
        likes = 0
        # print(like)
        # checking if we found any like
        if len(like) == 0: 
            return likes
        else:
            return cls(like[0])

    # this method edit like entry in the database
    @classmethod
    def update_like(cls,data):
        query = "UPDATE likes SET count = %(count)s WHERE show_id = %(id)s" 
        connectToMySQL(Like.database_name).query_db(query,data)
        
    # this method gets number of users liking a specific show
    @classmethod
    def get_likers(cls,data):
        query = "SELECT COUNT(user_id) FROM likes WHERE show_id = %(id)s"
        user_counts_per_show = connectToMySQL(Like.database_name).query_db(query,data)
        count = user_counts_per_show[0]["COUNT(user_id)"]
        # print (f"*********count is:{count}")
        return count
    