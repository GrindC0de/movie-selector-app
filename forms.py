from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UserAddForm(FlaskForm):

    ## this form adds a new user. all data is required in order to sign up and if something is left blank an error will be displayed.

    username = StringField('Username', validators=[DataRequired(message="This field is required")])
    first_name = StringField('First Name', validators=[DataRequired(message="This field is required")])
    last_name = StringField('Last Name', validators=[DataRequired(message="This field is required")])
    email = StringField('E-mail', validators=[DataRequired(message="This field is required"), Email()])
    password = PasswordField('Password', validators=[DataRequired(message="This field is required"),Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="This field is required"), EqualTo('password', message=('Passwords must match'))])
    submit = SubmitField('Sign Up')

class UserEditForm(FlaskForm):

    ## this form allows a user to edit their information

    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=8)])

class LoginForm(FlaskForm):

    ## this login form checks user credentials and if something is not filled out an error will return
    
    username = StringField('Username', validators=[DataRequired(message="Username cannot be blank")])
    password = PasswordField('Password', validators=[DataRequired(message="Password cannot be blank"), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RateMovie(FlaskForm):

    ## this form saves the title and rating of a movie

    title = StringField('Movie', validators=[DataRequired()])
    rating = SelectField("Rating", choices=[(1, 'Terrible'), (2, 'Not Good'), (3, 'Good'), (4, 'Pretty Good'), (5, 'Excellent')], coerce=int)