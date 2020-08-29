#!/usr/bin/python3
import json
import dominate
from dominate.tags import *
from os import listdir
from os.path import isfile, join

#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
#https://github.com/Knio/dominate

def get_user_stories(file_path):
    with open(file_path) as user_story_json_file:
        data = json.load(user_story_json_file)
        return data

def generate_story_div(page_body, user_name, entries_data):
    for entry_data in entries_data:
        entry_div = div(id=user_name + "-" + entry_data['date'], cls="userStory")
        with entry_div:
            header_div = div()
            with header_div:
                span(user_name, cls="userName")
                span(entry_data['date'], cls="storyDate")
            br()
            p(entry_data['content'])
        page_body.add(entry_div)
        #print(entry_div)

def generate_story_view(page_body, path):
    json_files = [f for f in listdir(path) if isfile(join(path, f))]
    for user_file in json_files:
        path_to_user_file = path + user_file
        json_data = get_user_stories(path_to_user_file)
        entries_data = json_data['entries']
        entries_data.reverse()
        #merge and sort all stories so feed is in reverse chronological order
        generate_story_div(page_body, user_file[0:-5], entries_data)


def my_function(name):
    try:
        with open("../data/" + name + ".json") as json_file:
            print("Adventures of " + name + "<br/><br/>")
            data = json.load(json_file)

            for entry in data["entries"]:
                print(entry["date"] + ": ")
                print(entry["content"]  + "<br/>")
    except:
        print("He has no adventures. Sad.")
    print("<br/><br/>")

page_body = body()
generate_story_view(page_body, "../data/")
print(page_body)
#my_function("garrett")
#my_function("masaya")
