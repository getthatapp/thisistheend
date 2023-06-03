from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# tworzymy instancje klasy Flask
app = Flask(__name__)
# ladujemy konfiguracje aplikacji z klasy Config
app.config.from_object(Config)
# tworzymy instancję SQLAlchemy, która reprezentuje bazę danych
db = SQLAlchemy(app)
# tworzymy instancję Migrate, która umożliwia wykonywanie migracji bazy danych
migrate = Migrate(app, db, render_as_batch=True)
# tworzymy instancję LoginManager, która ułatwia zarządzanie sesjami użytkowników
login = LoginManager(app)
# określamy nazwę widoku, do którego użytkownik zostanie przekierowany,
# jeśli nie jest zalogowany i próbuje uzyskać dostęp do zasobów wymagających uwierzytelnienia
login.login_view = 'login'

from blog import routes, models
from blog import fake_data


@login.user_loader  # dekorator
# Ta funkcja jest używana do ładowania obiektu użytkownika na podstawie jego identyfikatora
def load_user(user_id):
    from blog.models import User
    return User.query.get(int(user_id))


@app.shell_context_processor # dekorator
# a funkcja zwraca słownik, który definiuje kontekst powłoki.
def make_shell_context():
    return {
        "db": db,
        "Entry": models.Entry
    }


@app.cli.command('generate-fake-data') # dekorator, który rejestruje funkcję jako komendę CLI (Command Line Interface
def generate_fake_data_command():
    user_id = input("Enter user ID: ")
    how_many = input("How many entries create?: ")
    fake_data.generate_entries(user_id=int(user_id), how_many=int(how_many))
    print("Generated fake data")
