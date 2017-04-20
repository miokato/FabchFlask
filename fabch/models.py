from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime
# from flask.ext.bcrypt import Bcrypt

from fabch import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(20), unique=True, index=True)
    _password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50),unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def _get_password(self):
        return self._password
    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        user = query(cls).filter(cls.email==email).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User%r>' % (self.username)



class Lectures(db.Model):
    __tablename__ = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    clsid = db.Column(db.Integer)
    cls = db.Column(db.Text)
    clsdesc = db.Column(db.Text)
    lecid = db.Column(db.Integer)
    lec = db.Column(db.Text)
    lecdesc = db.Column(db.Text)
    url = db.Column(db.Text)
    lecurl = db.Column(db.Text)
    movid = db.Column(db.Integer)

    def __repr__(self):
        return '<Classes id={id} title={title!r}>'.format(
                id=self.id, title=self.title)
    
def init():
    db.create_all()
