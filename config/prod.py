import os

DEBUG = False
SECRET_KEY = 'asdfrgrgoo'
UPLOAD_PATH = 'uploads'
OUTPUT_PATH = 'output'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False
ALLOWED_EXTENSIONS = {'txt', 'pdf'}
