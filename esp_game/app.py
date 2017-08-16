# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import logging
from logging import Formatter, FileHandler

from flask import render_template, request
from flask_login import login_user, login_required, logout_user, current_user

from esp_game import app
import esp_game.api_functions as func
from esp_game.models import init_db
from esp_game.forms import *


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    return func.login(form, login_user)


@login_required
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    form = RegisterForm(request.form)
    return func.logout(current_user, logout_user, form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    return func.register(form)


@app.route('/task', methods=['GET', 'POST'])
def task():
    return func.task(current_user)


@app.route('/task/run', methods=['GET', 'POST'])
def taskrun():
    task_id = int(request.form.get('task_id'))
    return func.get_task(task_id, current_user)


@app.route('/task/save', methods=['GET', 'POST'])
def tasksave():
    task_id = int(request.form.get('task_id'))
    primary_id = int(request.form.get('primary_id'))
    secondary_ids = request.form.getlist('secondary_ids')
    return func.task_save(task_id, current_user, primary_id, secondary_ids)



# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    init_db()
    app.run(use_reloader=True)
