from app import app, db
from app.forms import LoginForm, NewPostForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Post

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = NewPostForm()
    posts = Post.query.filter_by(user_id=current_user.id)
    return render_template('index.html', title='Home Page', posts=posts, form=form)

@app.route('/newpost', methods=['POST'])
@login_required
def newpost():
    form = NewPostForm(request.form)
    post = Post(body=form.text.data, user_id=current_user.id)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    app.logger.info(request.form)
    if "bomb" in request.form:
        return render_template('bomb.html')
    return render_template('about.html')
