import os
from app import secret
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-password'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # FLASK_DEBUG=1
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    SECURITY_EMAIL_SENDER = 'newbredun95new@gmail.com'

    ADMINS = ['newbredun95new@gmail.com']

    POSTS_PER_PAGE = 2

    LANGS = ['en', 'ru', 'uk']
    MS_TRANSLATOR_KEY = secret.translate_key

    ELASTIC_SEARCH = secret.ELASTIC_SEARCH

