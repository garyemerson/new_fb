#!/usr/bin/python3

import sqlite3
from datetime import datetime
from pytz import timezone

sql_data_file_path = "/home/app/doc_root/erryday/prototype/data/data.sqlite"
cmd_get_all_records = """
    select post.id, author, text, upload_time_unix_ms, GROUP_CONCAT(post_image.id, ',')
    from post
        left join post_image on post.id = post_image.post_id
    group by post.id
    order by upload_time_unix_ms desc"""
# TODO: maybe change order to be day instead of upload time?

def retrieve_records():
    raw_records_list = __get_records_from_sql()
    return __translate_to_records_object(raw_records_list)

def __get_records_from_sql():
    with sqlite3.connect(sql_data_file_path) as conn:
        c = conn.cursor()
        c.execute(cmd_get_all_records)
        return c.fetchall()

def __translate_to_records_object(raw_records_list):
    translated_list = []
    for record_tuple in raw_records_list:
        translated_list.append(dict({
            'id': record_tuple[0],
            'author': record_tuple[1],
            'text': record_tuple[2],
            'timestamp': datetime.fromtimestamp(record_tuple[3]/1000.0).astimezone(timezone('US/Pacific')).strftime("%Y-%m-%d %I:%M %p"),
            'images': record_tuple[4] #need to convert this to a list
        }))
    return translated_list