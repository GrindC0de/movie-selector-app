from flask import Flask, render_template, flash, redirect, request, session, jsonify, make_response, url_for
from flask_debugtoolbar import DebugToolbarExtension
from random import randint
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_manager, login_user, current_user, logout_user, login_required
from forms import LoginForm, UserEditForm, UserAddForm, RateMovie
from models import db, connect_db, User, RatedMovies, Bcrypt
import requests
import pdb

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ypiywnwehsyndp:f8399ecfe03ad0064475d8b8ac7c9ab9a918f174ce42add92027189d9f8727a6@ec2-3-232-163-23.compute-1.amazonaws.com:5432/dfh3ur4r8k4utl'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "very-secret"
toolbar = DebugToolbarExtension(app)


API_KEY = "98003250cab93815401d6d3944d8a675"
connect_db(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.init_app(app)

#### LOGIN/LOGOUT SECTION

@login_manager.user_loader
def load_user(user_id):
    ## Checks to see if the user has been logged in. If they are, they will not have to sign in
    return User.query.get(int(user_id))

@app.route('/', methods=["GET", "POST"])
def base():
    ## this is the homepage. The form checks against the LoginForm for when a user fills it out. If they do something wrong an error o is returned in an object. If the login is successful the /profile page will load

    form = LoginForm()
    errors = {}

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect("/profile")
        
    else:        
        print(form.errors)
        
    return render_template('base.html', form=form)

@app.route('/login', methods=["POST"])
def login():
    ## returns to homepage
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    ## uses the flask-login to logout the user by checking to see if they are first logged in. Once the user logs out they are redirected to the homepage.
    logout_user()
    flash("You have been logged out.", 'success')
    return redirect("/")

##SIGN UP/PROFILE SECTION

@app.route('/signup', methods=["GET", "POST"])
def signup():
    ## using flask-login, the application checks to see if the user is already logged in, if they are it redirects them to the profile page.
    if current_user.is_authenticated:
        return redirect("/profile")

    ## the form checks info against the form.py. If the user fills out all the correct information and submits the form, they are added to the database. Their password is also Bcrypt-hashed. It also checks against usernames and emails to make sure there are no repeats.
    form = UserAddForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user_obj = User.query.filter_by(username=form.username.data).first()
        if user_obj:
            flash(f"That username is already taken.", "warning")

        email_obj = User.query.filter_by(email=form.email.data).first()
        if email_obj:
            flash(f"That email has been used.", "warning")

        
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        login_user(new_user)
        flash(f'Welcome, {form.username.data}!', 'success')
        return redirect("/profile")
    else:
        ## if there are errors, the error will flash and the page will be reloaded.
        print(form.errors)

    
        return render_template('signup.html', form=form)
        

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    ## using flask-login, the page checks to see if the user is already logged in with login_required. If they are the page loads the user profile from the database. 

    form = UserEditForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Success! Information updated!', 'success')
        return redirect('/profile')
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email

        return render_template('profile.html', form=form)


## FIND A FILM/RATE A FILM/VIEW WATCHED FILMS

@app.route('/findafilm', methods=["GET", "POST"])
@login_required
def find_a_film():
    
    ## this page loads a random movie with a frontend javascript component. if the user clicks that they want to watch a film, the front end submits the form and they are taken to a rate-film page.
    
    form = RateMovie()

    return render_template('findafilm.html', form=form)


@app.route('/rate-film', methods=["POST"])
@login_required
def rate_film():

    ## this page also makes sure the user is logged in. When this page loads, it loads the last randomly selected film that the frontend javascript picked. 

    form = RateMovie()
    movieData = request.form.get('data')
    movieJson = []


    ## if the movieData is not equal to None, the movieJson will load the movieData and render a json format of movieData.
    if movieData != None:
        movieJson = json.loads(movieData)
        return render_template("rate-film.html", form=form, movieJson=movieJson)

    ## once the user submits a rating on the film, the title, rating, user_id, and add_movie are submitted to the database and saved there so that they can later be displayed in a "rated films" section.
    if form.validate_on_submit():
        title = request.form.get('title')
        print(title)
        rating = request.form.get("rating")
        print(rating)
        user_id = current_user.id
        add_movie = RatedMovies(title=title, rating=rating, user_id=user_id)
        db.session.add(add_movie)
        db.session.commit()
                
        return redirect("/ratedfilms")
    
    ## if there is an error, the form error will flash
    print(form.errors)
    return render_template("rate-film.html", form=form, movieJson=movieJson)



@app.route('/ratedfilms', methods=['GET', 'POST'])
@login_required
def rated_films():
    ## Rated Films should simply display the films rated for the user. Once the page is loaded it will reach into the Postgres database and display all of the films by rating. 
    rated_films = RatedMovies.query.get(title, rating).order_by(rating).all()
    return render_template('ratedfilms.html', rated_films=rated_films)

## Displays a 404 error if the user invokes it

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


## Displays a 400 error if the user invokes it

@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html', e=e), 400


if __name__ == '__main__':
    app.run(debug=True)
