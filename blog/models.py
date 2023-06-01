from flask import url_for
from blog import db
import datetime


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Entry {}>'.format(self.title)

    def get_absolute_url(self):
        return url_for('entry_detail', entry_id=self.id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Entry', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)