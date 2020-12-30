from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectMultipleField, FieldList, FormField, FileField
from wtforms.fields.html5 import DateTimeLocalField, DateField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import datetime, date

from otherFiles.setup import *
from otherFiles.databases import *

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', validators=[DataRequired(),
                                Length(min=2, max=20)])

    name = StringField('Store Name', validators=[DataRequired(), Length(min=4,max=50)])
    addressNum = IntegerField('Address Number', validators=[DataRequired(), NumberRange(min=1000, max=9999)])
    addressStreet = StringField('Address Street', validators=[DataRequired(), Length(max=50)])
    addressCity = StringField('City', validators=[DataRequired(), Length(max=50)])
    zipCode = IntegerField('Zip Code', validators=[DataRequired(), NumberRange(min=10000, max=99999)])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        store = Store.query.filter_by(username=username.data).first()
        if store:
            raise ValidationError('That username is taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class DateRange(Form):
    # start = StringField('Name of Item', validators=[DataRequired(), Length(min=2, max=50)])
    # end = StringField('Name of Item', validators=[DataRequired(), Length(min=2, max=50)])
    start = DateTimeLocalField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end = DateTimeLocalField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

class AddItem(FlaskForm):
    name = StringField('Name of Item', validators=[DataRequired(), Length(min=2, max=50)])
    cost = DecimalField('Cost of Item (Dollars - Item will be 80% off when sold.)', validators=[DataRequired()])
    category = SelectMultipleField('Item Category', choices=[('Protein', 'Protein'), ('Dairy', 'Dairy'),('Fruits', 'Fruits'),('Vegetables', 'Vegetables'),('Grains','Grains')], validators=[DataRequired()])
    weight = DecimalField('Weight of Item (lbs)', validators=[DataRequired()])
    sellBy = DateField('Sell By Date', format='%Y-%m-%d', validators=[DataRequired()], default=date.today)
    expiration = DateField('Actual Expiration Date', format='%Y-%m-%d', validators=[DataRequired()])
    pickupTimes = FieldList(FormField(DateRange, label=""), min_entries=1, label="Pick Up Times")
    picture = FileField('Food Picture',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Add Item')
    # pickupTimes = ('Pickup', backref='item', lazy=True)

class Purchase(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=50)])
    pickupTimes = SelectMultipleField('Pickup Time', validators=[DataRequired()])
    submit = SubmitField('Purchase Now')

