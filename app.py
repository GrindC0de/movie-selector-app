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
    return User.query.get(int(user_id))

@app.route('/', methods=["GET", "POST"])
def base():
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
    
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", 'success')
    return redirect("/")

##SIGN UP/PROFILE SECTION

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/profile")

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
            return render_template("/", form=email_obj)  
        
        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash(f'Welcome, {form.username.data}!', 'success')
        return redirect("/profile")
    else:
        print(form.errors)

    
        return render_template('signup.html', form=form)
        

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    
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


##FIND A FILM/RATE A FILM/VIEW WATCHED FILMS

@app.route('/findafilm', methods=["GET", "POST"])
@login_required
def find_a_film():

    return render_template('findafilm.html')


@app.route('/rate-film', methods=["POST"])
@login_required
def rate_film():
    
    movieData = request.form['data']
    movieJson = json.loads(movieData)

    form = RateMovie()

    if form.validate_on_submit():
        title = request.headers.get("title")
        rating = request.form.get("rating")
        add_movie = RatedMovies(title=title, rating=rating)
        db.session.add(add_movie)
        db.session.commit()
        print(title, rating)
        
        return redirect("/ratedfilms")

    print(movieJson)

    return render_template("rate-film.html", movieJson=movieJson)

@app.route('/ratedfilms')
@login_required
def rated_films():
    rated_films = RatedMovies.query.order_by('rated_movies').all()
    return render_template('ratedfilms.html', rated_films=rated_films)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
