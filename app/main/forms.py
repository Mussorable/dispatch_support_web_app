from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

import sqlalchemy as sa

from app import db
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TruckForm(FlaskForm):
    truck_number = StringField('Truck Number', validators=[DataRequired()])
    trailer_number = SelectField(
        'Trailer Number',
        choices=[('', 'None (Select)')]
    )
    submit = SubmitField('Truck')


class TrailerForm(FlaskForm):
    trailer_number = StringField('Trailer Number', validators=[DataRequired()])
    truck_number = SelectField(
        'Truck Number',
        choices=[('', 'None (Select)')]
    )
    submit = SubmitField('Trailer')
