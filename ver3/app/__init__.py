from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
moment = Moment(app)

login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
