import os
from config import Config


def test_config():
    config = Config()

    assert isinstance(config.DEBUG, bool)
    assert isinstance(config.SECRET_KEY, str)
    assert isinstance(config.SQLALCHEMY_DATABASE_URI, str)
    assert isinstance(config.SQLALCHEMY_TRACK_MODIFICATIONS, bool)


def test_config_defaults():
    config = Config()

    assert config.SECRET_KEY == 'you-will-never-guess'
    assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:////Users/gtest/Desktop/py_books/kodilla_py/thisistheend/blog_app.db'


def test_config_from_env_vars(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test_secret_key')
    monkeypatch.setenv('DATABASE_URL', 'test_database_url')

    config = Config()

    assert config.SECRET_KEY == 'test_secret_key'
    assert config.SQLALCHEMY_DATABASE_URI == 'test_database_url'


def test_sqlalchemy_track_modifications():
    config = Config()

    assert config.SQLALCHEMY_TRACK_MODIFICATIONS is False

