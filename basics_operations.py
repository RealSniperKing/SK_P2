# -*- coding: utf-8 -*-
import os
import os.path
import re


# BASIC OPERATIONS
def count_element_in_list(items, element):
    items_count = []
    for i_elem, item in enumerate(items, 0):
        if item == element:
            items_count.append(item)
    return items_count


def count_directories_parents(path):
    try:
        path_split = path.split('../')
        value_parents = count_element_in_list(path_split, '')
        count = len(value_parents)
    except:
        count = 0
    return count


def merge_link_to_url(url, link):
    url_split = url.split('/')
    value = count_directories_parents(link)

    for i in range(0, value + 1):
        del url_split[len(url_split) - 1]

    path_ok = convert_array_to_string(url_split, '/') + '/' + link.replace('../', '')

    return path_ok


def convert_array_to_string(tableau, separator):
    new_line = ''
    for i, elem in enumerate(tableau, 0):
        if i == 0:
            new_line += str(elem)
        else:
            new_line += str(separator) + str(elem)
    return new_line


def add_folder(path_root_folder, name_new_folder):
    tempo_new_folder = os.path.join(path_root_folder, name_new_folder)
    if not os.path.exists(tempo_new_folder):
        try:
            os.makedirs(tempo_new_folder)
        except:
            print('This folder already exist')
    return tempo_new_folder


def remove_all_special_characters(string_item):
    cleaned_string = re.sub(r"[-()\"#/@;:<>{}`+=~|.!?,*]", "", string_item)
    return cleaned_string
