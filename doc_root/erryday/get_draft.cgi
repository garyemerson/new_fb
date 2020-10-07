#!/usr/bin/python3

import os, sqlite3

print('Content-type: text/plain\r\n\r\n', end='')

# Hi G$
# Hola!

# print("foobar")
# os.exit()

parts = os.environ['QUERY_STRING'].split("=")
if parts[0] != "author":
    raise Exception('Only \'author\' param supported but found \'{}\''.format(parts[0]))
if parts[1] == "":
    raise Exception('author param can\'t be empty')
author = parts[1]
# print("author: {}".format(author))
with sqlite3.connect('data/data.sqlite') as conn:
    c = conn.cursor()
    c.execute('''
        SELECT text from post
        where date(upload_time_unix_ms / 1000, 'unixepoch') = date('now')
            and author = ?''',
        (author,))
    row = c.fetchone()
    if row: print(row[0])
