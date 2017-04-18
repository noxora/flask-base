#!flask/bin/python

import os
from flask import Flask, render_template_string
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter

#Using a class-based config to avoid a second file
#I will be using a second file later
class ConfigClass(object):
    #Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'THIS IS AN INSECURE SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///basic_app.sqlite')
    CSRF_ENABLED = True

    #Flask-Mail Things
    MAIL_USERNAME =           os.getenv('MAIL_USERNAME',        'ldecker499@gmail.com')
    MAIL_PASSWORD =           os.getenv('MAIL_PASSWORD',        'password')
    MAIL_DEFAULT_SENDER =     os.getenv('MAIL_DEFAULT_SENDER',  '"MyApp" <noreply@example.com>')
    MAIL_SERVER =             os.getenv('MAIL_SERVER',          'smtp.gmail.com')
    MAIL_PORT =           int(os.getenv('MAIL_PORT',            '465'))
    MAIL_USE_SSL =        int(os.getenv('MAIL_USE_SSL',         True))

    #Flask-User settings
    USER_APP_NAME = "Appname"

def create_app():
    #Setup Flask
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')

    #Initialize extensions
    db = SQLAlchemy(app)
    mail = Mail(app)

    #Define the user model
    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), nullable=False, unique=True)
        password = db.Column(db.String(255), nullable=False, server_default='')
        #Email info
        email = db.Column(db.String(255), nullable=False, unique=True)
        confirmed_at = db.Column(db.DateTime())
        #User info
        active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
        first_name = db.Column(db.String(100), nullable=False, server_default='')
        last_name = db.Column(db.String(100), nullable=False, server_default='')
    #Make the database tables
    db.create_all()

    #Setup Flask User
    db_adapter = SQLAlchemyAdapter(db, User) #Register the user model?
    user_manager = UserManager(db_adapter, app) #Start Flask-User

    #Make the home page
    @app.route("/")
    def home_page():
       return render_template_string("""
            {% extends "base.html" %}
            {% block content %}
                <h2>Home page</h2>
                <p>This page can be accessed by anyone.</p><br/>
                <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
                <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
                {% endblock %}
            """)
    @app.route("/members")
    @login_required
    def members_page():
        return render_template_string("""
        {% extends "base.html" %}
        {% block content %}
            <h2>Members page</h2>
            <p>This page can only be accessed by authenticated users.</p><br/>
            <p><a href={{ url_for('home_page') }}>Home page</a> (anyone)</p>
            <p><a href={{ url_for('members_page') }}>Members page</a> (login required)</p>
        {% endblock %}
        """)

    return app

if __name__ =='__main__':
    app=create_app()
    app.run(debug=True)
