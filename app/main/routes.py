from flask import render_template, current_app

from app.main import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template(
        'index.html',
        title='Home',
        website_title=current_app.config['WEBSITE_TITLE'],
    )
