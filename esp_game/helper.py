import constants as cons
from models import *


def get_sortd_scndry_imgs_by_previous_votes(primary_id, scndry_imgs_id_list):
    """
    Function to return the sorted list of secondary images id on the basis
    of the previous votes given by the users.
    :param scndry_imgs_id_list: List of secondary images id to sort
    :return: Sorted list of secondary images id
    """
    return PrimarySecondaryMapping.query \
        .with_entities(PrimarySecondaryMapping.secondary_id) \
        .filter(PrimarySecondaryMapping.secondary_id.in_(scndry_imgs_id_list),
                PrimarySecondaryMapping.primary_id == primary_id) \
        .order_by(PrimarySecondaryMapping.related_votes.desc()).all()


def get_sorted_imgs_dict(prm_image_id, scndry_imgs_id_url_dict):
    """
    Function to return the list of secondary images first sorted by the response given
    by the other user and then sorted by the previous votes given to the secondary
    image.
    :param task: Task object created right after starting the game
    :param current_user: Current user provided by flask-login
    :param secondary_imgs_id:list of secondary images is
    :return: Sorted list of secondary images , containing id and url
    """
    sorted_imgs = get_sortd_scndry_imgs_by_previous_votes(prm_image_id, scndry_imgs_id_url_dict)
    return [(img_id[0], scndry_imgs_id_url_dict[img_id[0]]) for img_id in sorted_imgs]


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


def update_user_points(db, current_user, scndry_ids, prm_id):
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
    task_list = Task.query\
        .filter(Task.primary_image_id == prm_id)
    scndry_ids_dict = {}
    for task in task_list:
        scndry_ids_tuple = tuple(sorted(map(int,task.secondary_images.split(' '))))
        if scndry_ids_dict.has_key(scndry_ids_tuple):
            scndry_ids_dict[scndry_ids_tuple]+=1
        else:
            scndry_ids_dict[scndry_ids_tuple]=1
    max_count = 0
    max_scndry_ids_tuple=()
    print scndry_ids_dict
    for scndry_ids_tuple,count in scndry_ids_dict.iteritems():
        if count > max_count:
            max_count = count
            max_scndry_ids_tuple = scndry_ids_tuple
    for task in task_list:
        print max_scndry_ids_tuple, tuple(sorted(map(int, task.secondary_images.split(' '))))
        if max_scndry_ids_tuple == tuple(sorted(map(int,task.secondary_images.split(' ')))):
            task.player_ans_in_set=True
        else:
            task.player_ans_in_set=False
        db.session.add(task)
    current_user.points = Task.query\
        .filter(Task.player_id == current_user.id, Task.player_ans_in_set)\
        .count()
    db.session.add(current_user)
    update_votes_for_scndry_imgs(db, scndry_ids, prm_id)


def update_votes_for_scndry_imgs(db, scndry_ids, prm_id):
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

