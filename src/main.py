# -*- coding: utf-8 -*-

import requests
from utils.credentials import promt_user_and_pass
from utils.scrap import login_into_uc3m, get_list_of_grades_from_directory, prepare_grade_for_iteration, iterate_pages_and_get_alumni_list
from utils.coding import convert_dict_list_to_ascii
from utils.saving import save_grades_to_csv, alumni_from_grade_is_already_saved, save_alumni_to_csv

import warnings
warnings.filterwarnings('ignore')

import logging
#logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('\033[93m%(asctime)s\033[0m:\033[94m%(name)s\033[0m:\033[92m%(levelname)s\033[0m:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    user, password = promt_user_and_pass()
    session = requests.Session()
    add_ssl_hack(session)
    login_into_uc3m(session, user, password)
    grades = get_list_of_grades_from_directory(session)
    grades_ascii = convert_dict_list_to_ascii(grades)
    save_grades_to_csv(grades_ascii, 'degree_list.csv')
    iterate_over_grades_and_save_alumni_data(session, grades_ascii)


def add_ssl_hack(session):

    # From http://stackoverflow.com/a/14146031/3149679
    from requests.adapters import HTTPAdapter
    from requests.packages.urllib3.poolmanager import PoolManager
    import ssl

    class MyAdapter(HTTPAdapter):
        def init_poolmanager(self, connections, maxsize, block=False):
            self.poolmanager = PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLSv1
            )

    session.mount('https://', MyAdapter())


def iterate_over_grades_and_save_alumni_data(session, grades):
    num_grades = len(grades)
    for i, grade in enumerate(grades):
        logger.info('Degree {}/{}: {}'.format(i + 1, num_grades, grade['name']))
        if alumni_from_grade_is_already_saved(grade['code'], 30):
            logger.info('Grade already saved')
            continue
        payload = prepare_grade_for_iteration(session, grade['code'])
        alumni_list = iterate_pages_and_get_alumni_list(session, payload)
        alumni_list_ascii = convert_dict_list_to_ascii(alumni_list)
        save_alumni_to_csv(alumni_list_ascii, grade['code'])


if __name__ == '__main__':
    main()
