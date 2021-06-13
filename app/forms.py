from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField,PasswordField,BooleanField,FileField
from wtforms.validators import DataRequired,Email,ValidationError,Length,EqualTo
from flask_login import current_user
from app.models import Users


class RequestQuoteForm(FlaskForm):
    fullname = StringField('Company name/Individual', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    phonenumber = StringField('Phone number', validators=[DataRequired()])
    producttype = SelectField(u'Product type', choices=[('Office supplies', 'Office supplies'), 
     ('Stationery', 'Stationery'),
     ('Building construction materials', 'Building construction materials'),
     ('Furniture and equipment supplies','Furniture and equipment supplies'),
     ('Water works, Tiling, Roofing and Plumbing materials','Water works, Tiling, Roofing and Plumbing materials'),
     ('Road construction materials supplies','Road construction materials supplies'),
     ('Industrial and institutional chemical supplies','Industrial and institutional chemical supplies'),
     ('Pest control and fumigation supplies and services','Pest control and fumigation supplies and services'),
     ('Industrial safety','Industrial safety'),
     ('Steam and steam fitting supplies','Steam and steam fitting supplies'),
     ('General hardware materials','General hardware materials'),
     ('Manufacturing plants and equipment','Manufacturing plants and equipment'),
     ('Medical supplies and equipment','Medical supplies and equipment'),
     ('Cleaning agents and equipment','Cleaning agents and equipment'),
     ('CCTV security and bio-metric door access systems','CCTV security and bio-metric door access systems'),
     ('Fresh and Dry food stuffs and diary products','Fresh and Dry food stuffs and diary products'),
     ('Electrical general supplies','Electrical general supplies'),
     ('Electronics and accessories supplies','Electronics and accessories supplies'),
     ('ICT and computers and accessories general supplies','ICT and computers and accessories general supplies')
     ])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update profile picture')
    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email does not exist!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AddCareerForm(FlaskForm):
    name = StringField('Career name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Add career')

class UpdateCareerForm(FlaskForm):
    name = StringField('Career name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Update career info')

class CompanyDetailsResetForm(FlaskForm):
    details = TextAreaField('Update content', validators=[DataRequired()])
    submit = SubmitField('Update')