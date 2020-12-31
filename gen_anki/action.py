#!/usr/bin/env python
# coding=utf-8

import sys
from orgpython import to_html
from generate_anki import create_note, create_deck, create_package, generate_anki_file

def is_question(line_data):
    if ':question:' in line_data:
        return True
    else:
        return False


def is_outline(line_data):
    if line_data[0] == '*':
        return True
    else:
        return False


def get_outline_level(line_data):

    level = 0
    for c in line_data:
        if c == '*':
            level = level + 1
        else:
            return level


def file_to_list(file_path):
    with open(file_path, 'r') as f:
        # line_data_list = [line.strip() for line in f.readlines()]
        line_data_list = f.readlines()

    return line_data_list

def delete_enter(line_data):
    return line_data.strip()


def get_question_content(line_data):
    begin = line_data.find(' ')
    end = line_data.rfind(' ')
    question_content = line_data[begin+1:end]

    return question_content


def get_outline_content(line_data):
    begin = line_data.find(' ')
    outline_content = line_data[begin+1:]

    return outline_content

def merge_parent(child_data, parent_list):
    for parent in reversed(parent_list):
        if parent is None:
            continue

        child_data = "{0}--{1}".format(parent, child_data)

    data = child_data
    return data


def gen_anki(question_answer_list):

    note_list = list()
    for question_answer in question_answer_list:
        question_content = question_answer["question"]
        answer_content = question_answer["answer"]

        answer_html = to_html(answer_content, toc=True, offset=0, highlight=True)

        note = create_note(question_content, answer_html)
        note_list.append(note)

    deck = create_deck(20201230, 'Test', note_list)

    package = create_package(deck)

    file_name = 'output.apkg'
    generate_anki_file(package, file_name)



def delete_child_outline(outline_list, outline_level):
    for i in range(len(outline_list)):
        if i >= outline_level:
            outline_list[i] = None

    return outline_list


def process(line_data_list):

    parent_list =  [None] * 10

    current_question_content = None
    current_question_outline_level = None
    current_answer_content = ''

    question_answer_list = list()

    for line_data in line_data_list:
        if len(line_data) == 0:
            continue

        if current_question_content != None:
            if is_outline(line_data):
                outline_level = get_outline_level(line_data)
                if outline_level <= current_question_outline_level:
                    question_answer = dict()
                    question_answer["question"] = current_question_content
                    question_answer["answer"] = current_answer_content
                    question_answer_list.append(question_answer)

                    current_question_content = None
                    current_question_outline_level = None
                    current_answer_content = ''
                    parent_list = delete_child_outline(parent_list, outline_level)
                else:
                    current_answer_content  = current_answer_content + line_data
            else:
                current_answer_content  = current_answer_content + line_data



        if is_question(line_data):
            current_question_outline_level = get_outline_level(line_data)
            current_question_content = get_question_content(line_data)
            current_question_content = delete_enter(current_question_content)
            parent_list = delete_child_outline(parent_list, current_question_outline_level)
            current_question_content = merge_parent(current_question_content, parent_list)

        elif is_outline(line_data):
            outline_level = get_outline_level(line_data)
            outline_content = get_outline_content(line_data)
            parent_list = delete_child_outline(parent_list, outline_level)
            parent_list[outline_level] = delete_enter(outline_content)

    gen_anki(question_answer_list)


def main():

    line_data_list = file_to_list(sys.argv[1])

    process(line_data_list)


main()
