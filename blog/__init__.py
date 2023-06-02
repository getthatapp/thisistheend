from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'

from blog import routes, models
from blog import fake_data


@login.user_loader
def load_user(user_id):
    from blog.models import User
    return User.query.get(int(user_id))


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Entry": models.Entry
    }


@app.cli.command('generate-fake-data')
def generate_fake_data_command():
    user_id = input("Enter user ID: ")
    how_many = input("How many entries create?: ")
    fake_data.generate_entries(user_id=int(user_id), how_many=int(how_many))
    print("Generated fake data")
