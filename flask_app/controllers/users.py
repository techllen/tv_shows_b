from flask_app import app
from flask import render_template,redirect,session,request
from flask_app.models import show, user
from flask import flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

# this route redirect users to the index/home page
@app.route("/")
def home():
    return render_template("index.html")

# this route handles user registration
@app.route("/register", methods = ["POST"])
def register():
    # validate inputs
    if not user.User.user_validation(request.form):
        # if any user input is invalid send the user to login page
        return redirect("/")
    else:
        #hashing passwords
        password_hash = bcrypt.generate_password_hash(request.form["password"])
        # print(password_hash)
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            #assigning the password hash into the password dictionary key    
            "password": password_hash
        }
        # saving the data
        user_id = user.User.register_user(data)
        # assigning session to the user
        session["user_id"] = user_id
    return redirect("/dashboard")

# this route handles user login
@app.route("/login", methods = ["POST"])
def login():
    # validating log in credentials inputs
    if not user.User.user_login_validation(request.form):
        return redirect("/")
    data = {
        "email": request.form["email"],
    }
    found_user = user.User.verify_user(data)
    if not found_user or not bcrypt.check_password_hash(found_user.password,request.form["password"]):
        user.User.get_error_message()
        return redirect("/")
    #assigning session to the user
    session["user_id"] = found_user.id
    return redirect("/dashboard")

# this route direct the user to the dashboard page
@app.route("/dashboard")
def dashboard():
    if session.get("user_id") == None: 
        return redirect("/")
    else: 
        is_available = show.Show.get_all_shows_with_users()
        # checking for empty database output
        if not is_available:
            # let the user know that the database is empty for now and they can add the first show
            flash("OOOOOOOOPS NO TV SHOW FOR NOW, YOU CAN PROCEED TO ADD THE FIRST SHOW IN THE LIST","banner")
            return render_template("new_show.html")
        # proceed to dashboard if no empty data
        else:
            data = {
                "id": session["user_id"]
            }
            return render_template("dashboard.html",user_to_display = user.User.get_one_user_by_id(data),shows_to_display = show.Show.get_all_shows_with_users())
    
# this route clears the sessions and redirect user to login page
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# this route redirects the user to the error page if the links is not found
@app.errorhandler(404)
def errors(e):
    return render_template("errorpage.html")