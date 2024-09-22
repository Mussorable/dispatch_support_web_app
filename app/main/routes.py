from urllib.parse import urlsplit

from flask import render_template, current_app, flash, redirect, url_for, request
from flask_login import current_user, logout_user, login_required, login_user

import sqlalchemy as sa

from app import db
from app.main import bp
from app.logic.map import generate_map
from app.main.forms import LoginForm, RegistrationForm
from app.models import User


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    interactive_map = generate_map()

    return render_template(
        'index.html',
        title='Home',
        website_title=current_app.config['WEBSITE_TITLE'],
        map=interactive_map,
    )


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            flash(f'{form.email.data} {form.password.data}')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template(
        'login.html',
        title='Log In',
        website_title=current_app.config['WEBSITE_TITLE'],
        form=form,
    )


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))

    return render_template(
        'register.html',
        title='Register',
        website_title=current_app.config['WEBSITE_TITLE'],
        form=form
    )