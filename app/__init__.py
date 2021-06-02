from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = '92660847ee989c815a32b5ecbad887f7'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///kevinsons.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'info@kevinsonssupply@gmail.com'
app.config['MAIL_PASSWORD'] = ''
mail = Mail(app)

from app import routes