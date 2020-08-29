#!/usr/bin/python3

import sys
import os
sys.path.insert(1, '/home/app/doc_root/erryday/prototype/data')
import records_helper #TODO: A better way to manage imports?

import json
from dominate.tags import *

def get_records_list():
    query_string = os.environ.get("QUERY_STRING")
    if query_string:
        #is there some kind of library that we can use to parse the query params?
        qslist = query_string.split("=") #fix this
        author = qslist[1] #fix this
        return records_helper.retrieve_records_by_author(author)
    return records_helper.retrieve_records()

def generate_feed_view(feed_div):
    records_list = get_records_list()
    if not records_list:
        with feed_div:
            div("No entries found", cls="user-post")
    else:
        for record in records_list:
            with feed_div:
                generate_post_div(record)

def generate_post_div(post):
    post_div = div(id=post['id'], cls="user-post")
    with post_div:
        header_div = div()
        with header_div:
            link = "/erryday/prototype?user=" + post['author'] #use some kind of url builder lib?
            a(span(post['author'], cls="header author"), href=link)
            span(post['day'], cls="header post-date")
        
        br()
        
        content_div = div()
        with content_div:
            p(post['text'])
        
        footer_div = div()
        with footer_div:
            span("Add stuff for interaction here?", cls="footer")
            span(post['timestamp'], cls="footer timestamp")

    return post_div

feed_div = div(id='feed', cls="feed-view")
generate_feed_view(feed_div)
print(feed_div)
qs = os.environ.get("QUERY_STRING")
print(qs)


# Why are you commenting on commented out code?

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
