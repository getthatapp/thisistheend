from flask import render_template, request
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    PER_PAGE = 5
    entries = Entry.query.order_by(Entry.pub_date.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    return render_template('entries.html', entries=entries)


@app.route('/new-post/', methods=['GET', 'POST'])
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published = form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
        else:
            errors = form.errors
    return render_template('entry_form.html', form=form, errors=errors)