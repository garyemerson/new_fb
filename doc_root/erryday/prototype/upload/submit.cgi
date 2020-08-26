#!/usr/bin/python3

import cgi, sys, sqlite3, re
from functools import reduce
from datetime import date, datetime, timezone

def log(s):
    with open("log", "a") as f:
        f.write(s + "\n")

def setup_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS post (
            id                      INTEGER PRIMARY KEY,
            upload_time_unix_ms     REAL NOT NULL,
            author                  TEXT NOT NULL,
            day                     TEXT NOT NULL,
            text                    TEXT)''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS post_image (
            id          INTEGER PRIMARY KEY,
            post_id     INTEGER NOT NULL)''')

def save_data(author, date, text, imgs):
    with sqlite3.connect('../data/data.sqlite') as conn:
        setup_tables(conn)
        c = conn.cursor()
        c.execute('''
            INSERT INTO post (author, day, text, upload_time_unix_ms)
            VALUES (?, ?, ?, CAST((strftime('%s','now') || substr(strftime('%f','now'), 4)) AS INTEGER))''',
            (author, date, text))
        post_id = c.lastrowid
        for img in imgs:
            c.execute("INSERT INTO post_image (post_id) VALUES (?)", (post_id,))
            img_filename = c.lastrowid
            with open("images/" + str(img_filename), "wb") as f: f.write(img)
        conn.commit()

def valid_date(date_str):
    if not re.match(r"^\d\d\d\d-\d\d-\d\d$", date_str):
        return "date must be of form XXXX-XX-XX, found {}".format(date_str)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return "failed to parse '{}' as date".format(date_str)
    curr_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if date_str > curr_date:
        return "cannot post for a day in the future"
    return None

def get_data():
    form = cgi.FieldStorage()
    author = form.getfirst("author")
    date = form.getfirst("date")
    date_err = valid_date(date)
    if date_err:
        fail(400, date_err)
    text = form.getfirst("text")
    imgs = reduce(list.__add__, [form.getlist(k) for k in form if k.startswith("img")], [])
    return (author, date, text, imgs)

def fail(status, msg):
    print('Status: {}\r\n'.format(status), end='')
    print('Content-type: text/plain\r\n\r\n', end='')
    print(msg)
    sys.exit()

with open("log", "w") as f: f.write("")

author, date, text, imgs = get_data()
save_data(author, date, text, imgs)

log("author: {}".format(author))
log("date: {}".format(date))
log("text: {}".format(text))
log("#imgs: {}".format(len(imgs)))

print("Content-type: application/octet-stream\r\n\r\n", end="")