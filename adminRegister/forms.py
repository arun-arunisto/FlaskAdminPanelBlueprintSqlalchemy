from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, length

class AdminRegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Password Must be Equal")])
    submit = SubmitField("Register")

class AdminLoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login")
