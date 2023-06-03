from flask import render_template, request, redirect, url_for, flash
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from blog import app, db
from blog.models import Entry, User
from blog.forms import EntryForm, RegistrationForm, LoginForm


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password!', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('`you have successfully logged in.', 'success')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('index'))


@app.route('/', defaults={'page': 1})
@app.route('/page/<int:page>')
def index(page):
    PER_PAGE = 15
    entries = Entry.query.order_by(Entry.pub_date.desc()).paginate(page=page, per_page=PER_PAGE, error_out=False)
    return render_template('entries.html', entries=entries)


@app.route('/new_post/', methods=['GET', 'POST'])
@login_required
def create_entry():
    form = EntryForm()
    errors = None
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
                db.session.commit()
                flash('Your post was successfully added!', 'success')
            except:
                flash('There was an error adding your post. Please try again.', 'danger')
                db.session.rollback()
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('new_post.html', form=form)


@app.route('/post/<int:entry_id>')
def entry_detail(entry_id):
    entry = Entry.query.filter_by(id=entry_id).first_or_404()
    return render_template('entry_detail.html', entry=entry)


@app.route('/edit_post/<int:entry_id>', methods=['POST', 'GET'])
@login_required
def edit_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    form = EntryForm(obj=entry)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                form.populate_obj(entry)
                db.session.commit()
                flash('Your post has been updated successfully!', 'success')
            except:
                flash('There was an error updating your post. Try again.', 'danger')
                db.session.rollback()
            return redirect(url_for('entry_detail', entry_id=entry.id))
    return render_template('edit_entry.html', form=form, entry_id=entry_id)


@app.route('/delete_post/<int:entry_id>', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    try:
        db.session.delete(entry)
        db.session.commit()
        flash("Your post has been successfully deleted!", 'success')
    except:
        db.session.rollback()
        flash('There was an error deleting your post. Please try again.', 'danger')
    return redirect(url_for('index'))