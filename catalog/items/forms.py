from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextField
from wtforms.validators import DataRequired, NumberRange


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    quantity = IntegerField(
        'Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category_id = IntegerField(
        'Category', validators=[DataRequired(), NumberRange(min=1)])
