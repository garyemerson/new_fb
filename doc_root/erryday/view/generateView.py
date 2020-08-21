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

def generate_story_div(file_path, user_name, json_data):
    entries_data = json_data['entries']
    entries_data.reverse()
    for entry_data in entries_data:
        entry_div = div(id=user_name + entry_data['date'])
        with entry_div:
            span(user_name)
            span(entry_data['date'])
            br()
            p(entry_data['content'])
        print(entry_div)
    print('test')

def generate_story_view(path):
    story = div(id='first div')
    with story:
        p("First dominate div")
        br()
    print(story)
    json_files = [f for f in listdir(path) if isfile(join(path, f))]
    for user_file in json_files:
        path_to_user_file = path + user_file
        json_data = get_user_stories(path_to_user_file)
        generate_story_div(path_to_user_file, user_file[0:-5], json_data)
    print(json_files)


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

my_function("garrett")
my_function("masaya")
generate_story_view("../data/")