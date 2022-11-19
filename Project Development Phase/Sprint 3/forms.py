from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class profileform(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    number = StringField('Phone Number', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    submit = SubmitField('Add')

class Editprofileform(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired()])
    place = StringField('Place', validators=[DataRequired()])
    number = StringField('Phone Number', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    submit = SubmitField('Edit')
    