"""URL Shortener"""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from Model import User

import string
import random

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "urls"

##############################################################################


@app.route('/')
def login():
    """Log-in"""
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def check_login():
    """Checks user login information against the db"""
    #Get POST request information from the /login page
    email = request.form.get('email')
    password = request.form.get('password')

    # Make a query to see if the users email and password are in the db
    user = User.query.filter_by(email=email).first()

    # If they are in the db, add them to a session and redirect home
    if user:
        if password == user.password:
            session['logged_in'] = user.user_id
            flash("Logged in")
            return redirect("/")
        else:
            flash("Login failed")
            return redirect("/")
    else:
        flash("please register here")
        return redirect("/register")


@app.route('/register')
def register():
    """renders registration template"""
    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def add_info():
    """Saves users registration information in the db"""

    # Get user information from registration form input
    #  FIXME: need to add users level & ride pref
    name = request.form.get('fname')
    email = request.form.get('email')
    password = request.form.get('password')

    # Query to see if users email and password are already in the db
    user = User.query.filter_by(email=email).first()

    # If they are in the db redirect to log in. If not save info to db
    if user:
        flash('User email already has an account')
        return redirect('/')
    else:
        new_user = User(fname=fname, lname=lname,
                        email=email, password=password)
        flash('Welcome')
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = new_user.user_id

        for category_id in checkboxes:
            new_cat = CatUser(user_id=new_user.user_id, category_id=category_id)
            db.session.add(new_cat)
        db.session.commit()

        return redirect('/')


@app.route('/logout')
def log_out_user():
    """Log out user"""

    session.clear()
    flash("Logged out")
    return redirect("/")


@app.route('/shorten')
def URL_shorten():
    """Shorten URLs to format http://bitly/userid/randsamp"""
    # store short URLs in db
    return redirect("/")


@app.route('/redirect', methods=['POST'])
def URL_redirect():
    """redirect to long URL"""
    # query db for long url
    # whenever this short URL is clicked on, redirect to a long URL
    # count click rate
    return redirect("/<long_url>")






##############################################################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    app.run(port=3000, host='0.0.0.0')