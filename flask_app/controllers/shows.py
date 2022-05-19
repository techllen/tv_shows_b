from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import show, user,like
from flask_app.controllers import users,likes

# this route redirect users add a show page
@app.route("/new")
def new_show():
    # check if user is logged in
    if session.get("user_id")==None:
        return redirect("/")
    else:
        return render_template("new_show.html")
# this route saves a show to the database
@app.route("/save_show",methods = ["POST"])
def save_show():
    # check if user is logged in
    if session.get("user_id")==None:
        return redirect("/")
    else:
        # validate show inputs
        if show.Show.validate_show_inputs(request.form) == False:
            return render_template("new_show.html")
        else:
            show_data = {
                "title":request.form["title"],
                "network":request.form["network"],
                "release_date":request.form["release_date"],
                "description":request.form["description"],
                "id" : session["user_id"]
            }
            # save the show to the database
            show.Show.save_show(show_data)
            return redirect ("/dashboard")
# this method retrieves show from the database for edit
@app.route("/edit/<int:id>")
def get_show_for_editing(id):
     # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        data = {
            "id" : id,
        }
        return render_template ("edit_show.html",show_to_display = show.Show.get_one_show_by_id(data))
# this route update a show in a database
@app.route("/update",methods = ["POST"])
def update_show():
    # validating inputs from show form
    show_id = request.form["show_id"]
    if show.Show.validate_show_inputs(request.form) == False:
        return redirect(f"/edit/{show_id}")
    else:
        # getting all info from the edit form
        show_data = {
            "title":request.form["title"],
            "network":request.form["network"],
            "release_date":request.form["release_date"],
            "description":request.form["description"],
            "id" : request.form["show_id"]
        }
        show.Show.update_show(show_data)
        
    return redirect ("/dashboard")
# this route show show details
@app.route("/show/<int:id>")
def show_show(id):
    # check if user is logged in
    if session.get("user_id")==None: 
        return redirect("/")
    else: 
        show_data = {
            "id" : id
        }
        return render_template ("tv_show_show.html",show_to_display = show.Show.get_one_show_with_user(show_data),count_to_display = like.Like.get_likers(show_data))
# this method delete show in the database
@app.route("/shows/delete/<int:id>")
def delete_show(id):
    data = {
        "id" : id
    }
    show.Show.delete_show(data)
    return redirect ("/dashboard")