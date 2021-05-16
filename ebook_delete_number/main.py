#!/usr/bin/env python
# coding=utf-8

import os
import sys


def delete_suf_number(string):
    dot_index = string.rfind('.')
    start_num_index = dot_index

    for i in range(dot_index-1, 0, -1):
        if not string[i].isdigit():

            start_num_index = i
            break

    new_string = string[:start_num_index+1] + string[dot_index:]

    return new_string

            

dir_path = sys.argv[1]

file_list = os.listdir(dir_path)

for file_name in file_list:
    new_file_name = delete_suf_number(file_name)
    os.rename(os.path.join(dir_path, file_name), os.path.join(dir_path, new_file_name))

