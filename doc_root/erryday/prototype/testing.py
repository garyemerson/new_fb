#!/usr/bin/python3
import json

#https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
#https://github.com/Knio/dominate
with open("testInput.json") as json_file:
    data = json.load(json_file)

    for user in data["users"]:
        print(user["name"] + "<br/>")
        for entry in user["entries"]:
            for image in entry["images"]:
                print("<img height=\"50\" src=" + image + "/><br/>")
            print(entry["content"]  + "<br/><br/><br/>")

    with open("upload/data", "r") as f:
        print(f.read())
