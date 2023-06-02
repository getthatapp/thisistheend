from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired
from blog.models import User


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Tytuł posta"})
    body = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Treść posta"})
    is_published = BooleanField('Is Published?')
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter your email address"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email address is already in use')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"placeholder": "Enter email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')