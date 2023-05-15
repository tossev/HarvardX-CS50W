from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=50)])    
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(LoginForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class SearchForm(FlaskForm):
    choices = [("isbn", "ISBN"),
               ("title", "Title"),
               ("author", "Author")]
    select = SelectField("Search by:", choices=choices)
    search = StringField("Looking for:", validators=[DataRequired()])
    submit = SubmitField('Search')
    
class Comment(FlaskForm):
    ratings = [("1", "1"),
               ("2", "2"),
               ("3", "3"),
               ("4", "4"),
               ("5", "5")]
    rate = SelectField("Rate:", choices=ratings)
    comment = TextAreaField("What do you think?", validators=[DataRequired()], render_kw={'autofocus': True})
    submit = SubmitField('Submit review')