from flask import render_template, request

import constants as cons
from models import *
from esp_game import db, login_manager


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
    task = Task.query.filter(Task.player2_id == None).first()
    if task:
        if current_user.id != task.player1_id:
            task.player2_id = current_user.id
        elif current_user.id == task.player1_id and task.player1_answer_count == 5:
            task = Task(current_user.id)
    else:
        task = Task(current_user.id)
    db.session.add(task)
    db.session.commit()
    return get_task(task.id, current_user)











# This Function can be broken down into smaller functions but because of
# time constraint , i am leaving it for now
def get_task(task_id, current_user):
    """
    Function to return a primary image and its seconday corresponding to the task
    :param task_id: Id of the task
    :param current_user: Current user provided by flask-login
    :return: Renders a page containing primary images and secondary images
    """
    task = Task.query.get(task_id)
    if current_user.id == task.player1_id:
        primary_image_id = task.primary_images_id.split(' ')[task.player1_answer_count]
    elif current_user.id == task.player2_id:
        primary_image_id = task.primary_images_id.split(' ')[task.player2_answer_count]
    else:
        raise Exception('Unauthorised User')
    primary_url = PrimaryImage.query.with_entities(PrimaryImage.id, PrimaryImage.url). \
        filter_by(id=primary_image_id)
    secondary_images_id = PrimarySecondaryMapping.query.with_entities(
        PrimarySecondaryMapping.secondary_id).filter_by(primary_id=primary_image_id)
    secondary_urls = SecondaryImage.query\
        .with_entities(SecondaryImage.id,SecondaryImage.url)\
        .filter(SecondaryImage.id.in_(secondary_images_id))\
        .all()
    return render_template("pages/question.html", task_id=task.id, urls=secondary_urls,
                           url=primary_url[0])






# This Function can be broken down into smaller functions but because of
# time constraint , i am leaving it for now
def task_save(task_id, current_user, primary_id, secondary_ids):
    """
    Function to save the user's set of selected secondary images.
    This function performs a few more tasks like:
    1> Updates the total answer count for a particular task by current user
    2> Updates the related_votes for primary-seconday image mapping.
       we will be using this mapping to show the related seconday images first
    3> Updates the user point if seconday images are same
    4> Saves the seconday image ids for a task's primary image

    :param task_id: Id of the task
    :param current_user:  Current user provided by flask-login
    :param primary_id: Primary image id
    :param secondary_ids: List of secondary images id selected by user
    :return: if last primary image , takes up to the start game page else
     Renders a page containing primary and secondary images
    """
    task = Task.query.get(task_id)
    if current_user.id == task.player1_id:
        task.player1_answer_count += 1
    elif current_user.id == task.player2_id:
        task.player2_answer_count += 1
    else:
        raise Exception('Unauthorised User')
    db.session.add(task)
    secondary_ids_str = " ".join(map(str, secondary_ids))
    task_run_by_other_player = TaskRun.query.filter(TaskRun.player_id != current_user.id,
                                                    TaskRun.task_id == task.id,
                                                    TaskRun.primary_id == primary_id).first()
    if task_run_by_other_player:
        if set(secondary_ids) == set(task_run_by_other_player.related.split(' ')):
            user = current_user
            user.points += 1
            other_user = User.query.get(task_run_by_other_player.player_id)
            other_user.points += 1
            for id in secondary_ids:
                pr_sec_mapping = PrimarySecondaryMapping.query.filter_by(primary_id=primary_id,
                                                                         secondary_id=int(
                                                                             id)).first()
                pr_sec_mapping.related_votes += 1
                db.session.add(pr_sec_mapping)
            db.session.add(other_user)
            db.session.add(user)
    task_run = TaskRun(task.id, current_user.id, primary_id, secondary_ids_str)
    db.session.add(task_run)
    if (current_user.id == task.player1_id and task.player1_answer_count == cons.TASK_IMAGES_COUNT) \
            or \
       (current_user.id == task.player2_id and task.player2_answer_count == cons.TASK_IMAGES_COUNT):
        task.status = 'success'
        db.session.add(task)
        db.session.commit()
        return render_template("pages/start_game.html")
    db.session.commit()
    return get_task(task_id, current_user)
