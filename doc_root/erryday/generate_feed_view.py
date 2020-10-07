#!/usr/bin/python3

import sys
import os
sys.path.insert(1, '/home/app/doc_root/erryday/data')
import records_helper #TODO: A better way to manage imports?

import json
from dominate.tags import *
from urllib.parse import parse_qs

def get_records_list():
    query_string = os.environ.get("QUERY_STRING")
    if query_string:
        qs_map = parse_qs(query_string)
        if (qs_map['author']):
            author = str(qs_map['author'][0])
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
            link = "/erryday?author=" + post['author'] #use some kind of url builder lib?
            a(span(post['author'], cls="header author"), href=link)
            span(post['day'], cls="header post-date")

        br()

        content_div = div()
        with content_div:
            p(post['text'])

        if post['images']:
            images_div_id = "images_" + str(post['id'])
            images_div = div(id=images_div_id, cls="images")
            with images_div:
                for image in post['images']:
                    image_path = "./upload/images/" + image
                    div(img(src=image_path, id=image, cls="image"), cls="slide")

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
