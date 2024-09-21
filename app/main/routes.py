from flask import render_template, current_app

from app.main import bp
from app.logic.map import generate_map


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
