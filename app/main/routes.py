from urllib.parse import urlsplit

from flask import render_template, current_app, flash, redirect, url_for, request
from flask_login import current_user, logout_user, login_required, login_user

import sqlalchemy as sa

from app import db
from app.main import bp
from app.logic.map import generate_map
from app.main.forms import LoginForm, RegistrationForm, TruckForm, TrailerForm
from app.models import User, Trailer, Truck


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


# Authentication endpoints
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
@login_required
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


# Navigation endpoints
@bp.route('/transport/<transport_type>')
@login_required
def transport(transport_type):
    return render_template(
        'transport-menu.html',
        title=transport_type.capitalize()[:-1],
        website_title=current_app.config['WEBSITE_TITLE'],
    )


@bp.route('/transport/<transport_type>/list')
@login_required
def transport_list(transport_type):
    transport_type = transport_type.capitalize()
    if transport_type not in ['Truck', 'Trailer']:
        flash('Incorrect transport type')
        return redirect(url_for('main.index'))

    return render_template(
        'transport-list.html',
        title=f'{transport_type[:-1]} List',
        website_title=current_app.config['WEBSITE_TITLE'],
    )


@bp.route('/transport/<transport_type>/add', methods=['GET', 'POST'])
@login_required
def transport_add(transport_type):
    transport_type = transport_type.capitalize()
    if transport_type not in ['Truck', 'Trailer']:
        flash('Incorrect transport type')
        return redirect(url_for('main.index'))

    if transport_type == 'Truck':
        form = TruckForm()
        # Load trucks numbers into SelectField choices, add them into existed list because None(truck) should be existed too
        trailers = db.session.scalars(sa.select(Trailer)).all()
        if trailers:
            form.trailer_number.choices.extend((trailer.trailer_number, trailer.trailer_number) for trailer in trailers)

        if form.validate_on_submit():
            truck = db.session.scalar(sa.select(Truck).where(Truck.truck_number == form.truck_number.data))
            if not truck:
                truck_number = form.truck_number.data
                trailer_number = form.trailer_number.data
                trailer = db.session.scalar(sa.select(Trailer).where(Trailer.trailer_number == trailer_number))

                truck = Truck(
                    truck_number=truck_number,
                    trailer=trailer,
                )
                db.session.add(truck)
                db.session.commit()
    else:
        form = TrailerForm()
        # Load trucks numbers into SelectField choices, add them into existed list because None(truck) should be existed too
        trucks = db.session.scalars(sa.select(Truck)).all()
        if trucks:
            form.truck_number.choices.extend((truck.truck_number, truck.truck_number) for truck in trucks)

        if form.validate_on_submit():
            trailer = db.session.scalar(sa.select(Trailer).where(Trailer.trailer_number == form.trailer_number.data))
            if not trailer:
                trailer_number = form.trailer_number.data
                truck_number = form.truck_number.data
                truck = db.session.scalar(sa.select(Truck).where(Truck.truck_number == truck_number))

                trailer = Trailer(
                    trailer_number=trailer_number,
                    truck=truck,
                )
                db.session.add(trailer)
                db.session.commit()

    return render_template(
        'transport-add.html',
        title=f'Add {transport_type}',
        type_of_transport=transport_type,
        website_title=current_app.config['WEBSITE_TITLE'],
        form=form,
    )
