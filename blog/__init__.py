from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db,render_as_batch=True)

from blog import routes, models
from blog import fake_data


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Entry": models.Entry
    }


@app.cli.command('generate-fake-data')
def generate_fake_data_command():
    fake_data.generate_entries()
    print("Generated fake data")