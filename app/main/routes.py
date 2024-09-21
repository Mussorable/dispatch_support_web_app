from flask import render_template, current_app, flash, redirect

from app.main import bp
from app.logic.map import generate_map
from app.main.forms import LoginForm


@bp.route('/')
@bp.route('/index')
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
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
        return redirect('/main.index')
    return render_template(
        'login.html',
        title='Log In',
        website_title=current_app.config['WEBSITE_TITLE'],
        form=form,
    )
