from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class EntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Tytuł posta"})
    body = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Treść posta"})
    is_published = BooleanField('Is Published?')
    submit = SubmitField('Submit')
