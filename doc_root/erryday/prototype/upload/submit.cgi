#!/usr/bin/python3

import cgi, sys, sqlite3
from functools import reduce

def log(s):
    with open("log", "a") as f:
        f.write(s + "\n")

def setup_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS post (
            id                      INTEGER PRIMARY KEY,
            upload_time_unix_ms     REAL NOT NULL,
            author                  TEXT,
            text                    TEXT)''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS post_image (
            id          INTEGER PRIMARY KEY,
            post_id     INTEGER NOT NULL)''')

def save_data(author, text, imgs):
    with sqlite3.connect('../data/data.sqlite') as conn:
        setup_tables(conn)
        c = conn.cursor()
        c.execute('''
            INSERT INTO post (author, text, upload_time_unix_ms)
            VALUES (?, ?, CAST((strftime('%s','now') || substr(strftime('%f','now'), 4)) AS INTEGER))''',
            (author, text))
        post_id = c.lastrowid
        for img in imgs:
            c.execute("INSERT INTO post_image (post_id) VALUES (?)", (post_id,))
            img_filename = c.lastrowid
            with open("images/" + str(img_filename), "wb") as f: f.write(img)
        conn.commit()

def get_data():
    form = cgi.FieldStorage()
    author = form.getfirst("author")
    text = form.getfirst("text")
    imgs = reduce(list.__add__, [form.getlist(k) for k in form if k.startswith("img")], [])
    return (author, text, imgs)

print("Content-type: application/octet-stream\r\n\r\n", end="")
with open("log", "w") as f: f.write("")

author, text, imgs = get_data()
save_data(author, text, imgs)

log("author: {}".format(author))
log("text: {}".format(text))
log("#imgs: {}".format(len(imgs)))
