from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app,db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique =True, nullable = False)
    profile_pic = db.Column(db.String(20), nullable = False, default = 'avatar.png')
    password = db.Column(db.String(100), nullable = False)
    admin = db.Column(db.Boolean, nullable = False, default = False)
   

    def get_reset_token(self,expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)


    def __repr__(self):
        return str(self.username) + str(self.email) + str(self.profile_pic)
        
class Careers(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))

    def __repr__(self):
        return str(self.name) + str(self.description)


class Company(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    mission = db.Column(db.String(255))
    vision = db.Column(db.String(255))
    company_focus = db.Column(db.String(255))

    def __repr__(self):
        return str(self.mission) + str(self.vision)+ str(self.company_focus)


class Images(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    image = db.Column(db.String(55))

    def __repr__(self):
        return str(self.image)
