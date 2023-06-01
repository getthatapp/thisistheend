import os


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(os.path.dirname(__file__), 'blog_app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
