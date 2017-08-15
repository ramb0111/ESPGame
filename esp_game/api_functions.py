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


def task(current_user):
    task = Task.query.filter(Task.player2_id == None).first()
    if task:
        if current_user.id != task.player1_id:
            task.player2_id = current_user.id
        elif current_user.id == task.player1_id and task.player1_answer_count == 5:
            task = Task(current_user.id)
    else:
        task = Task(current_user.id)
    print task.player1_id , task.player2_id
    db.session.add(task)
    db.session.commit()
    return get_task(task.id, current_user)


def get_task(task_id, current_user):
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
    secondary_urls = SecondaryImage.query.with_entities(SecondaryImage.id,
                                                        SecondaryImage.url).filter(
        SecondaryImage.id.in_(secondary_images_id)).all()
    return render_template("pages/question.html", task_id=task.id, urls=secondary_urls,
                           url=primary_url[0])


def task_save(task_id, current_user, primary_id, secondary_ids):
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
        print set(secondary_ids), set(task_run_by_other_player.related.split(' '))
        if set(secondary_ids) == set(task_run_by_other_player.related.split(' ')):
            user = current_user
            user.points += 1
            other_user = User.query.get(task_run_by_other_player.player_id)
            other_user.points += 1
            for id in secondary_ids:
                pr_sec_mapping = PrimarySecondaryMapping.query.filter_by(primary_id=primary_id, secondary_id=int(id)).first()
                pr_sec_mapping.related_votes += 1
                db.session.add(pr_sec_mapping)
            db.session.add(other_user)
            db.session.add(user)
    task_run = TaskRun(task.id, current_user.id, primary_id, secondary_ids_str)
    db.session.add(task_run)
    if (current_user.id == task.player1_id and task.player1_answer_count == cons.TASK_IMAGES_COUNT)\
            or \
        (current_user.id == task.player2_id and task.player2_answer_count == cons.TASK_IMAGES_COUNT):
        task.status = 'success'
        db.session.add(task)
        db.session.commit()
        return render_template("pages/start_game.html")
    db.session.commit()
    return get_task(task_id, current_user)