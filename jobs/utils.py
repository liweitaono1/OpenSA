#!/usr/bin/env python
# encoding: utf-8


"""
@version: ??
@author: wtli
@license: MIT Licence
@contact: 1135577502@qq.com
@site: https://
@software: PyCharm
@file: utils.py
@time: 2019-09-07
"""
import os

from OpenSA.settings import DATA_DIR


def list_upload_info(upload_id):
    file_info = {}
    upload_dir = '{}/upload/{}'.format(DATA_DIR,upload_id)
    file_list = os.listdir(upload_dir)
    for i in file_list:
        if os.path.isfile("{}/{}".format(upload_dir, i)):
            file_info.setdefault(i, "file")
        else:
            file_info.setdefault(i, "dir")

    return file_info
