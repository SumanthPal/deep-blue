from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes, models
#TODO: Work on init database

# @app.before_first_request
# def initialize_database():
#     models.init_db()
