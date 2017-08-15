from flask import render_template, request

from models import User
from esp_game import db, login_manager


@login_manager.user_loader
def user_loader(user_email):
    """Given *user_id*, return the associated User object.

    :param user_email: user_id's user to retrieve
    """
    return User.query.filter_by(email=user_email).one()


def register(form):
    if request.method == 'GET':
        return render_template('forms/register.html', form=form)
    elif request.method == 'POST':
        email = form.email.data
        if not email.endswith(tuple(['@gmail.com', ['@squadrun.com']])):
            return render_template('forms/register.html', form=form,
                                   message="Domain must be gmail.com or squadrun.com")
        if User.query.filter_by(email=form.email.data).first():
            return render_template('forms/register.html', form=form,
                                   message="Email address already exists")
        else:
            newuser = User(form.name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            return render_template('forms/login.html', form=form,
                                   message="User Created")


def login(form, login_user):
    if request.method == 'GET':
        return render_template('forms/login.html', form=form)
    elif request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.active = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return render_template('pages/start_game.html')
        else:
            return render_template('forms/login.html', form=form,
                                   message="User not exist")


def logout(current_user, logout_user, form):
    """Logout the current user."""
    user = current_user
    user.active = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("forms/login.html", form=form)
