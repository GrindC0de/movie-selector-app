from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    ## this table is the users table. it takes an id, first name, last name, email, and password which gets hashed by Bcrypt.

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String,
        nullable=False,
    )
    
    last_name = db.Column(
        db.String,
        nullable=False,
    )

    email = db.Column(
        db.String,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def signup(cls, username, email, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class RatedMovies(db.Model):

    ## this table is for rated movies adn takes the id, title, rating, and user_id

    __tablename__ = "rated_movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def serialize():
        return {
            'id': self._id,
            'title': self.title,
            'rating': self.rating
        }

    def __repr__(self):
        return f"<RatedMovies {self.id}, {self.title}, {self.rating}>"

def connect_db(app):

    db.app = app
    db.init_app(app)