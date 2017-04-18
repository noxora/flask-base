from flask_user import UserMixin
from app import db

#First make the user
class User(db.Model, UserMixin):
    __tablename__  = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #User authentication info for Flask-User
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable = False, server_default='')
    #Activity
    active = db.Column('curr_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(40), nullable=False, server_default='')
    last_name = db.Column(db.String(40), nullable=False, server_default='')

    #roles for Flask-User
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

#Define what a role means
class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default='', unique=True)
    label = db.Column(db.Unicode(255), server_default=u'')

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

