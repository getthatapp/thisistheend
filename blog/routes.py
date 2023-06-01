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
                is_published=form.is_published.data
            )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)


@app.route('/post/<int:entry_id>')
def entry_detail(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return render_template('entry_detail.html', entry=entry)


@app.route('/edit_post/<int:entry_id>', methods=['POST', 'GET'])
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    form = EntryForm(obj=entry)
    if request.method == "POST":
        if form.validate_on_submit():
            form.populate_obj(entry)
            db.session.commit()
            return redirect(url_for('entry_detail', entry_id=entry.id))
    return render_template('edit_entry.html', form=form, entry_id=entry_id)
