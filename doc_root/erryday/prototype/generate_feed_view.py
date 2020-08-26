#!/usr/bin/python3

import sys
sys.path.insert(1, '/home/app/doc_root/erryday/prototype/data')
import records_helper #TODO: A better way to manage imports?

import json
from dominate.tags import *

def generate_feed_view(feed_div):
    records_list = records_helper.retrieve_records()
    for record in records_list:
        with feed_div:
            generate_post_div(record)

def generate_post_div(post):
    post_div = div(id=post['id'], cls="userPost")
    with post_div:
        header_div = div()
        with header_div:
            span(post['author'], cls="userName")
            span(post['timestamp'], cls="postDate")
        br()
        p(post['text'])
    return post_div

feed_div = div(id='feed')
generate_feed_view(feed_div)
print(feed_div)

# Why is there commented out code here???
# Please add comments to your commented out code

#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
#https://github.com/Knio/dominate
# with open("testInput.json") as json_file:
#     data = json.load(json_file)

#     for user in data["users"]:
#         print(user["name"] + "<br/>")
#         for entry in user["entries"]:
#             for image in entry["images"]:
#                 print("<img height=\"50\" src=" + image + "/><br/>")
#             print(entry["content"]  + "<br/><br/><br/>")
