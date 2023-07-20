import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    def __init__(self):
        self.DEBUG = True
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
        self.SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'blog_app.db'))
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
