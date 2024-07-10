import os
from dotenv import load_dotenv, dotenv_values
from flask_login import login_manager

load_dotenv()
class Config:
    # Basic configuration settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    DATABASE = os.environ.get('DATABASE_URL')
