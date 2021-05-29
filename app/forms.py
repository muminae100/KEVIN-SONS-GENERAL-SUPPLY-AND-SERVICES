from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,ValidationError


class RequestQuoteForm(FlaskForm):
    fullname = StringField('Company name/Individual', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phonenumber = StringField('Phone number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
