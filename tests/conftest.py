import pytest
from blog import create_app, db
from blog.models import User, Entry


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    app_context = app.app_context()
    app_context.push()
    yield app
    app_context.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def _db(app):
    db.app = app
    db.create_all()
    yield _db
    db.drop_all()


@pytest.fixture
def user(_db):
    user = User(username='Test User', email='test@example.com')
    user.set_password('test_password')
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture
def entry(_db, user):
    entry = Entry(title='Test Entry', body='This is a test.', is_published=True, user_id=user.id)
    _db.session.add(entry)
    _db.session.commit()
    return entry
