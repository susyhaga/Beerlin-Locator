
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange, ValidationError
from beerlin.models import Local, Ranking







class PostForm(FlaskForm):

    list_bar = Local.store_list()
    list_beer = Ranking.beer_list()

    bar = SelectField('Bar', choices = list_bar, validators=[DataRequired()])
    
    beer = SelectField('Beer', choices = list_beer, validators=[DataRequired()])
    rank = IntegerField('Rank your experience (from 0 to 5)', validators=[NumberRange(min=0,max=5,message='Invalid number! Please rank from 0 to 5!')])
 


    submit = SubmitField('Save')

