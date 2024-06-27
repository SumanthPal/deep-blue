import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()
class Config:
    # Basic configuration settings
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Database configuration
    DATABASE = os.environ.get('DATABASE_URL') or 'database.db'
