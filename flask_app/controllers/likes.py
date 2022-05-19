from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import like, user
from flask_app.controllers import users,likes

# this route updates and saves a like to the database
@app.route("/like/<int:id>")
def add_like(id):
    # check if user is logged in
    if session.get("user_id")==None:
        return redirect("/")
    show_data = {
    "id" : id
    }
    # get the number of likes from database for show
    likes = like.Like.get_likes_by_show_id(show_data)
    if likes == 0:
        likes = likes + 1 
        like_data = {
            "count":likes,
            "user_id":session["user_id"],
            "show_id":show_data["id"]
        }
        # add the like to the total likes if the show has no likes
        like.Like.save_like(like_data)
    # if we already have likes update the database
    else:
    # get the likes
        likes = likes.count + 1
    # update likes for a specific show
        like_data = {
            "count":likes,
            "id":show_data["id"]
        }
        # if the show has likes already update likes
        like.Like.update_like(like_data)
    return redirect ("/dashboard")

# this route updates and saves a like to the database
@app.route("/unlike/<int:id>")
def reduce_like(id):
    # check if user is logged in
    if session.get("user_id")==None:
        return redirect("/")
    show_data = {
    "id" : id
    }
    # get the number of likes from database for show
    # if no likes yet for the show go back to the dashboard
    likes = like.Like.get_likes_by_show_id(show_data)
    if likes == 0:
        return redirect ("/dashboard")
    # if we already have likes update the database
    else:
    # get the likes
        # reduce the likes if the user has at least one like for the show
        if likes.count >= 1:
            likes = likes.count - 1
            # update likes for a specific show
            like_data = {
                "count":likes,
                "id":show_data["id"]
            }
            # if the show has likes already update likes
            like.Like.update_like(like_data)
        else:
            return redirect ("/dashboard")
    return redirect ("/dashboard")