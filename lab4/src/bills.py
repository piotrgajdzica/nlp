import os

import regex


def bills():
    data_dir = '../../lab1/data'
    for directory in os.listdir(data_dir):
        if directory.endswith('txt'):

            # if not directory.startswith("2003_1187"):
            yield directory.split('.')[0]
                # break