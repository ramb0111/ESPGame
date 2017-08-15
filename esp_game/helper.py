from random import sample
import constants as cons


def get_random_primary_images():
    """
    Function to return string containing 5 random ids from primary image table.
    :return: String containing 5 primary images id
    """
    random_list = sample(xrange(1,cons.PRIMARY_IMAGES_COUNT + 1),cons.TASK_IMAGES_COUNT)
    return " ".join(map(str, random_list))
