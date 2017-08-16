import pytest

from helper import get_random_primary_images
import constants as cons

def test_get_random_primary_images():
    """
    Test function to check iof all the ids are in range from 1 to 15
    :return:
    """
    ids_list = get_random_primary_images().split(' ')
    ids_list = map(int,ids_list)
    for id in ids_list:
        if not 1 <= id <= cons.PRIMARY_IMAGES_COUNT :
            assert False
    assert True