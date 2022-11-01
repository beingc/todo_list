# coding=utf8
# Date: 2022-11-01
# Desc: a to-do list app

import sys
import argparse
import sqlite3


def parser_args():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--add")
    group.add_argument("-u", "--update")
    group.add_argument("-c", "--complete")
    group.add_argument("-d", "--delete")
    group.add_argument("-s", "--show", action='store_true')
    group.add_argument("-r", "--reset", action='store_true')
    return parser.parse_args()


def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(""" create table todo_list 
    (todoid int,
    todoname text,
    createtime text,
    updatetime text,
    completetime text);""")


def add_todo(item):
    pass


def update_todo(item):
    pass


def complete_todo(item):
    pass


def delete_todo(item):
    pass


def show_todo():
    pass


def reset_todo():
    pass


if __name__ == '__main__':
    args = parser_args()
    init_db()
    if args.add:
        add_todo(args.add)
    if args.delete:
        delete_todo(args.delete)
    if args.update:
        update_todo(args.update)

# todo: do it now
