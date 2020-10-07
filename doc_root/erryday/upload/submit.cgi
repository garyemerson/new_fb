#!/usr/bin/python3

import cgi, sys, sqlite3, re
from functools import reduce
from datetime import date, datetime, timezone

def log(s):
    with open("log", "a") as f:
        f.write(s + "\n")

def setup_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id                      INTEGER PRIMARY KEY,
            upload_time_unix_ms     REAL NOT NULL,
            author                  TEXT NOT NULL,
            day                     TEXT NOT NULL,
            text                    TEXT NOT NULL,
            img_ids                 TEXT)''')

def save_data(author, date, text, imgs):
    with sqlite3.connect('../data/records.sqlite') as conn:
        setup_tables(conn)
        c = conn.cursor()
        c.execute('''
            INSERT INTO records (author, day, text, img_ids, upload_time_unix_ms)
            VALUES (?, ?, ?, ?, CAST((strftime('%s','now') || substr(strftime('%f','now'), 4)) AS INTEGER))''',
            (author, date, text, None))


        img_list = []
        new_record_id = c.lastrowid
        img_index = 0
        for img in imgs:
            img_filename = str(new_record_id) + "_" + str(img_index)
            with open("images/" + str(img_filename), "wb") as f: f.write(img)
            img_list.append(img_filename)
            img_index += 1

        if len(img_list) > 0:
            img_list_string = ','.join(map(str, img_list))
            c.execute('''
                UPDATE records
                SET img_ids = ?
                WHERE
                    id = ?''',
                (img_list_string, new_record_id))
        conn.commit()

# return error str if bad date, None if good date
def valid_date(date_str):
    if not re.match(r"^\d\d\d\d-\d\d-\d\d$", date_str):
        return "date must be of form YYYY-MM-DD, found {}".format(date_str)
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
