from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from models import db

app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecretkey"
app.config['Spostgres://pxumoiupfjuhci:90f20f17e786d402b581f8ed1591ab6d075047c19d26ebd82789f557c3297955@ec2-54-83-61-142.compute-1.amazonaws.com:5432/dcqt9oeni90gkq'] = "postgresql://project1:123password@localhost/project1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

#upload folder
UPLOAD_FOLDER = "./app/static/upload"

db = SQLAlchemy

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
