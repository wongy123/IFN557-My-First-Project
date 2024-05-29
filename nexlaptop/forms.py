from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional

class ContactForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    order_number = IntegerField('Order Number (if applicable)', validators=[Optional()])
    question = TextAreaField('Question*', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CheckoutForm(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    address = TextAreaField('Address*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    phone = StringField('Phone*', validators=[DataRequired()])
    submit = SubmitField('Submit Order')

class ViewOrderForm(FlaskForm):
    order_id = IntegerField('Order ID', validators=[DataRequired()])
    submit = SubmitField('View Order')
