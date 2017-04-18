from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_user import UserManager, SQLAlchemyAdapter 
from flask_wtf import CSRFProtect
from wtforms.fields import HiddenField

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
app.config['WTF_CSFR_ENABLED'] = True
CSRFProtect(app)
def is_hidden_field_filter(field):
    return isinstance(field, HiddenField)
app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field_filter

#Flask User
from app.models import User
from app.forms import SomeRegisterForm
from app.views import user_profile_page
db_adapter = SQLAlchemyAdapter(db,User)
user_manager = UserManager(db_adapter, app, register_form=SomeRegisterForm,
                            user_profile_view_function=user_profile_page)
from app import views, models
