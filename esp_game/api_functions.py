from flask import render_template, request

import constants as cons
from models import *
from esp_game import db, login_manager
from esp_game import helper as hl

@login_manager.user_loader
def user_loader(user_email):
    """Given *user_id*, return the associated User object.

    :param user_email: user_id's user to retrieve
    """
    return User.query.filter_by(email=user_email).first()


def register(form):
    """
    Function to register the user.
    :param form: Form containing user name , email and password
    :return: Renders template for login if successfull else renders register page with error
    message
    """
    if request.method == 'GET':
        return render_template('forms/register.html', form=form)
    elif request.method == 'POST':
        email = form.email.data
        if not email.endswith(tuple(['@gmail.com', '@squadrun.com'])):
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
    """
    Function to login the user
    :param form: Form containing user email and password
    :param login_user: login_user function from flask-login to update
           about the new user
    :return: Renders template for start game if successfull else renders login page with error
    message
    """
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
    """
    Function to logout the current user
    :param current_user: Current user provided by flask-login
    :param logout_user: logout user function from flask-login to logout the current user
    :return: Renders template for login
    """
    user = current_user
    user.active = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("forms/login.html", form=form)


def task(current_user):
    """
    Function to return a new task or an existing task.
    If player 1 is already assigned , returns an existing task
    else returns a new task
    :param current_user: Current user provided by flask
    :return: Task id and current user
    """
    hl.delete_task_if_not_completed(db, current_user)
    task = Task.query.filter(Task.player2_id == None).first()
    if task:
        if current_user.id != task.player1_id:
            task.player2_id = current_user.id
            db.session.add(task)
        else:
            task = Task(current_user.id)
            db.session.add(task)
    else:
        task = Task(current_user.id)
        db.session.add(task)
    db.session.commit()
    return get_task(task.id, current_user)


def get_task(task_id, current_user):
    """
    Function to return a primary image and its secondary images for a task
    :param task_id: Id of the task
    :param current_user: Current user provided by flask-login
    :return: Renders a page containing primary images and secondary images
    """
    task = Task.query.get(task_id)
    primary_image_id = hl.get_primary_image_id_from_task(task, current_user)
    primary_url = PrimaryImage.query.with_entities(PrimaryImage.id, PrimaryImage.url). \
        filter_by(id=primary_image_id)

    secondary_id_urls_dict = hl.get_scndry_img_id_url_dict(primary_image_id)
    sorted_scndry_id_url_list = hl.get_sorted_imgs_dict(task, current_user, primary_image_id,
                                                        secondary_id_urls_dict)
    return render_template("pages/question.html", task_id=task.id, urls=sorted_scndry_id_url_list,
                           url=primary_url[0])


def task_save(task_id, current_user, primary_id, secondary_ids):
    """
    Function to save the user's set of selected secondary images.
    :param task_id: Id of the task
    :param current_user:  Current user provided by flask-login
    :param primary_id: Id of Primary image
    :param secondary_ids: List of secondary images id selected by user
    :return: if last primary image , takes up to the start game page else
     Renders a page containing primary and secondary images
    """
    task = Task.query.get(task_id)
    hl.update_answer_count_for_player(task, current_user, db)
    task_run_by_other_player = hl.get_other_user_taskrun(task, current_user, primary_id)
    hl.update_user_points(db, task_run_by_other_player, current_user, secondary_ids, primary_id)
    secondary_ids_str = " ".join(map(str, secondary_ids))
    task_run = TaskRun(task.id, current_user.id, primary_id, secondary_ids_str)
    db.session.add(task_run)
    if hl.update_task_status(current_user, task, db):
        return render_template("pages/start_game.html")
    db.session.commit()
    return get_task(task_id, current_user)
