from flask import render_template, request, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    PER_PAGE = 5
    entries = Entry.query.order_by(Entry.pub_date.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    return render_template('entries.html', entries=entries)


@app.route('/new_post/', methods=['GET', 'POST'])
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
            return redirect(url_for('entries'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)