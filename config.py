import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    MONGODB_USER = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
    MONGODB_PASSWORD = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'mongo')
    MONGODB_PORT = os.environ.get('MONGODB_PORT', '27017')
    MONGODB_DB = os.environ.get('MONGO_INITDB_DATABASE', 'flask_blog')

    # Build URI với authSource=admin để xác thực user root
    MONGODB_URI = os.environ.get('MONGODB_URI')
