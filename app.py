from flask import Flask, render_template, flash, redirect, request, session, g, jsonify, make_response
from flask_debugtoolbar import DebugToolbarExtension
from random import randint
import json
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, UserEditForm, UserAddForm, RateMovie
from models import db, User, RatedMovies
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:toor@localhost:5432/movie_select'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "very-secret"
toolbar = DebugToolbarExtension(app)


API_KEY = "98003250cab93815401d6d3944d8a675"

#### LOGIN/LOGOUT SECTION

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        flash(f"Welcome back, {username}!", "success")
        return redirect("profile.html")

    else:
        flash("Invalid credentials.", 'danger')
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():

    flash("You have been logged out.", 'success')
    return redirect("/")

##SIGN UP/PROFILE SECTION

@app.route('/signup', methods=["GET", "POST"])
def signup():

    form = UserAddForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.email.data
        
        new_user = User(username=username, first_name=first_name, last_name=last_name, password=password)

        db.session.add(new_user)
        db.session.commit()
        return redirect("profile.html")
    else:
        return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
    user = User.username

    if not g.user:
        return redirect('login.html')
        
    return render_template('profile.html', user=user)

@app.route('/edit-profile', methods=["GET", "POST"])
def edit_profile():
    form = UserEditForm()

    if form.validate_on_submit():
        username = User.username.data
        email = User.email.data
        password = User.password.data
        db.session.commit()
        flash('Changes saved!')
        return redirect("profile.html")
    
    # elif request.method == 'GET':
    #     form.username = User.username
    #     form.email = User.email
    #     form.password = User.password
    return render_template('edit-profile.html', form=form)

##FIND A FILM/RATE A FILM/VIEW WATCHED FILMS

@app.route('/findafilm', methods=["GET", "POST"])
def find_a_film():
    return render_template('findafilm.html')


@app.route('/rate-film', methods=["POST"])
def rate_film():

    movieData = request.form['data']
    movieJson = json.loads(movieData)

    # form = RatedMovies()

    # title = request.args['film-title']
    # rating = request.args['rating']
    # db.add(title)
    # db.commit()

    return render_template("rate-film.html")

@app.route('/ratedfilms')
def rated_films():
    rated_films = RatedMovies.query.all()
    return render_template('ratedfilms.html', rated_films=rated_films)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)