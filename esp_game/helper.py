import constants as cons
from models import *


def get_primary_image_id_from_task(task, current_user):
    """
    Function to get id of the primary image from a given task object
    :param task: Task object created right after starting the game
    :param current_user: Current user provided by flask-login
    :return: Id of the primary image
    """
    if current_user.id == task.player1_id:
        primary_image_id = task.primary_images_id.split(' ')[task.player1_answer_count]
    elif current_user.id == task.player2_id:
        primary_image_id = task.primary_images_id.split(' ')[task.player2_answer_count]
    else:
        raise Exception('Unauthorised User')
    return primary_image_id


def update_answer_count_for_player(task, current_user, db):
    """
    Function to update the total answer count of the current player upto now
    :param task: Task object created right after starting the game
    :param current_user: Current user provided by flask-login
    :param db: SqlAlchemy object to update the current task
    """
    if current_user.id == task.player1_id:
        task.player1_answer_count += 1
    elif current_user.id == task.player2_id:
        task.player2_answer_count += 1
    else:
        raise Exception('Unauthorised User')
    db.session.add(task)


def get_sortd_scndry_imgs_by_previous_votes(scndry_imgs_id_list):
    """
    Function to return the sorted list of secondary images id on the basis
    of the previous votes given by the users.
    :param scndry_imgs_id_list: List of secondary images id to sort
    :return: Sorted list of secondary images id
    """
    return PrimarySecondaryMapping.query \
        .with_entities(PrimarySecondaryMapping.secondary_id) \
        .filter(PrimarySecondaryMapping.secondary_id.in_(scndry_imgs_id_list)) \
        .order_by(PrimarySecondaryMapping.related_votes.desc()).all()


def get_sorted_imgs_dict(task, current_user, prm_image_id, scndry_imgs_id_url_dict):
    """
    Function to return the list of secondary images first sorted by the response given
    by the other user and then sorted by the previous votes given to the secondary
    image.
    :param task: Task object created right after starting the game
    :param current_user: Current user provided by flask-login
    :param secondary_imgs_id:list of secondary images is
    :return: Sorted list of secondary images , containing id and url
    """
    other_user_task_run = get_other_user_taskrun(task, current_user, prm_image_id)

    imgs_selctd_by_othr_user=[]
    if other_user_task_run:
        imgs_selctd_by_othr_user = map(int, other_user_task_run.related.split(' '))
    imgs_not_selctd_by_othr_user = list(
        set(scndry_imgs_id_url_dict.keys()) - set(imgs_selctd_by_othr_user))
    sorted_imgs = get_sortd_scndry_imgs_by_previous_votes(imgs_selctd_by_othr_user)
    sorted_imgs.extend(get_sortd_scndry_imgs_by_previous_votes(imgs_not_selctd_by_othr_user))

    return [(img_id[0], scndry_imgs_id_url_dict[img_id[0]]) for img_id in sorted_imgs]


def get_other_user_taskrun(task, current_user, primary_image_id):
    """
    Function to return the TaskRun object for the other user participated
    in the given task.
    :param task: Task object created right after starting the game
    :param current_user: Current user provided by flask-login
    :param primary_image_id: Id of the primary image
    :return: TaskRun object
    """
    return TaskRun.query.filter(TaskRun.player_id != current_user.id,
                                TaskRun.task_id == task.id,
                                TaskRun.primary_id == primary_image_id).first()


def get_scndry_img_id_url_dict(primary_image_id):
    """
    Function to return dictionay of secondary images containing id and url as key and value
    respectively.
    :param primary_image_id: Id of the primary image
    :return: Dictionary of secondary images
    """
    secondary_imgs_id = PrimarySecondaryMapping.query.with_entities(
        PrimarySecondaryMapping.secondary_id).filter_by(primary_id=primary_image_id)

    return dict(SecondaryImage.query \
                .with_entities(SecondaryImage.id, SecondaryImage.url) \
                .filter(SecondaryImage.id.in_(secondary_imgs_id)) \
                .all()
                )


def update_user_points(db, task_run_by_other_player, current_user, scndry_ids, prm_id):
    """
    Function to update the points of both the user if each of them selects the same
    set of secondary images
    :param db: SqlAlchemy object to update the current task
    :param task_run_by_other_player: Boolean to check if there is other player
                                     participated or not upto now
    :param current_user: Current user provided by flask-login
    :param scndry_ids: List of secondary image ids
    :param prm_id: Id of the primary image
    """
    if task_run_by_other_player:
        if set(scndry_ids) == set(task_run_by_other_player.related.split(' ')):
            user = current_user
            user.points += 1
            other_user = User.query.get(task_run_by_other_player.player_id)
            other_user.points += 1
            db.session.add(user)
            update_votes_for_scndry_imgs(db, scndry_ids, prm_id, other_user)


def update_votes_for_scndry_imgs(db, scndry_ids, prm_id, other_user):
    """
    Function to update the votes of the secondary images if both the user
    chooses the same set of secondary images.
    :param db: SqlAlchemy object to update the current task
    :param scndry_ids: List of secondary image ids
    :param prm_id: Id of the primary image
    :param other_user: Other User Object for the same task
    :return:
    """
    for id in scndry_ids:
        pr_sec_mapping = PrimarySecondaryMapping.query.filter_by(primary_id=prm_id,
                                                                 secondary_id=int(
                                                                     id)).first()
        pr_sec_mapping.related_votes += 1
        db.session.add(pr_sec_mapping)
    db.session.add(other_user)


def update_task_status(current_user, task, db):
    """
    Function to update the status of the task to success , if current user
    answered all the 5 questions(i.e primary images)
    :param current_user: Current user provided by flask-login
    :param task: Task object created right after starting the game
    :param db: SqlAlchemy object to update the current task
    :return: Returns True if Task is successfully completed
    """
    if (current_user.id == task.player1_id and task.player1_answer_count == cons.TASK_IMAGES_COUNT) \
            or \
            (current_user.id == task.player2_id and task.player2_answer_count == cons.TASK_IMAGES_COUNT):
        task.status = 'success'
        db.session.add(task)
        db.session.commit()
        return True
    return False



def delete_task_if_not_completed(db, current_user):
    """
    Function to delete the task if not completed by the current user
    :param db: SqlAlchemy object to update the current task
    :param current_user: Current user provided by flask
    """
    task_not_completed = Task.query.filter(TaskRun.player_id == current_user.id,
                                           Task.player2_id == None,
                                           Task.player1_answer_count != 5).first()
    if task_not_completed:
        db.session.delete(task_not_completed)