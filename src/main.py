# coding=utf8
# Date: 2022-11-01
# Desc: a to-do list app

import time
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


def init_data():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(""" create table if not exists todo_list 
    (todoid int,
    todoname text,
    createtime text,
    updatetime text,
    completetime text);""")
    c.close()


def show_todo():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(""" select * from todo_list;""")
    values = c.fetchall()
    if values:
        print("{:>10} {:>20} {:>14} {:>14} {:>14}".format("todoid", "todoname", "createtime", "updatetime",
                                                          "completetime"))
        for i in values:
            print("{:>10} {:>20} {:>14} {:>14} {:>14}".format(i[0], i[1], i[2], i[3], i[4]))
    else:
        print("todo list is empty")
    conn.close()


def add_todo(item):
    todoid = int(time.time())
    todoname = item
    createtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    updatetime = ""
    completetime = ""
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("insert into todo_list(todoid, todoname, createtime, updatetime, completetime) values (?,?,?,?,?);",
              (todoid,
               todoname, createtime, updatetime, completetime))
    conn.commit()
    conn.close()


def reset_todo():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(""" drop table todo_list;""")
    conn.close()


def update_todo(item):
    pass


def complete_todo(item):
    pass


def delete_todo(item):
    todoname = item
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("delete from todo_list where todoname='{}'".format(todoname))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    args = parser_args()
    init_data()
    show_todo()
    if args.add:
        add_todo(args.add)
    if args.delete:
        delete_todo(args.delete)
    if args.update:
        update_todo(args.update)
    if args.reset:
        reset_todo()

# todo: a lot todo
