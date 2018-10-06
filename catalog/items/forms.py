from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, HiddenField
from wtforms.fields import TextAreaField
from wtforms.validators import ValidationError, DataRequired, NumberRange


class ItemForm(FlaskForm):
    """ Form used for Item creation and edition """
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField(
        'Description', validators=[DataRequired()],
        render_kw={'rows': 7, 'cols': 32})
    quantity = IntegerField(
        'Quantity', validators=[DataRequired(), NumberRange(min=0)])
    category_id = IntegerField(
        'Category', validators=[DataRequired(), NumberRange(min=1)])


class DeleteItemForm(FlaskForm):
    """
    Form used to delete item. It is mainly used to provide CSRF
    protection. Later on, this form will be modified to include
    item existence check.
    """
    action = HiddenField(default='delete_item', validators=[DataRequired()])

    def validate_action(form, field):
        if field.data != 'delete_item':
            raise ValidationError("This value should not be tampered with")
