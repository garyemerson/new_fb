#!/usr/bin/python3

# Import modules for CGI handling
import cgi, cgitb
import sys
import os
import json
from datetime import datetime
# import cgitb; cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
name = form.getvalue('name')
story = form.getvalue('story')

json_path = '../data/' + name + '.json'

json_data = {}
try:
    input_file = open(json_path, "r")
    json_data = json.load(input_file)
except:
    json_data.update({"entries": []})

json_entries = json_data['entries']
todays_entry = {"date" : str(datetime.now().strftime("%Y-%m-%d %I:%M %p")), "content" : story}
json_entries.append(todays_entry)
output_file = open(json_path, "w")
output_file.write(json.dumps(json_data, indent=4))

# with open("data", "wb") as f:
#     f.write(str.encode("NAME: {}<br/>\n".format(name)))
#     f.write(str.encode("STORY: {}\n".format(story)))
#     if os.path.isfile(json_path):
#         f.write(str.encode("File exists: {}".format(json_path)))

print("Content-type: application/octet-stream\r\n\r\n")
