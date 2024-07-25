import flask_wtf
import email_validator
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import EmailField, StringField, DecimalField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class user_registration(FlaskForm):
    """ make a registrationform with validation """
    firstname = StringField("Firstname", validators=[DataRequired(message="This is required"), Length(min=2, max=16)])
    surname = StringField("Surname", validators=[DataRequired(), Length(min=2, max=16)])
    phone = StringField('Phone Number', validators=[DataRequired(message="Enter Phone Number without the leading '0' digit e.g 723567937"), Length(min=9, max=9)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),
                                     Length(min=6), EqualTo('password')])
    buying_user =  BooleanField("I want to buy services on Labnerd?")
    selling_user = BooleanField("I want to sell services on Labnerd?")
    submit = SubmitField("Create account")


class user_login(FlaskForm):
    """ make a loginform with validation """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    session =  BooleanField('Stay signed in?')
    submit = SubmitField("LOGIN")

class instrument_enlist(FlaskForm):
    """ form for adding an instrument """
    name =  StringField("Name", validators=[DataRequired()])
    price_per_day = DecimalField('Price_per_day', validators=[DataRequired()])
    price_per_week =  DecimalField('Price_per_week')
    price_per_sample =  DecimalField('Price_per_sample', validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Length(min=20, max=200)])
    location = TextAreaField("Location", validators=[Length(min=20, max=200)])
    instrument_image = FileField("Photo_of_Instrument", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("ADD INSTRUMENT")
