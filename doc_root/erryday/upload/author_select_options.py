#!/usr/bin/python3

import sqlite3

print("<option disabled selected value>--</option>")
with sqlite3.connect('../data/records.sqlite') as conn:
    c = conn.cursor()
    c.execute("select distinct author from records")
    for author in c.fetchall():
        print("<option value=\"{a}\">{a}</option>".format(a = author[0]))
