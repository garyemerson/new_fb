#!/usr/bin/python3

# import sys, os
# with open("submit_request_raw_data", "wb") as f:
#     f.write("{}\nbody:\n".format(os.environ['CONTENT_TYPE']).encode('utf-8'))
#     f.write(sys.stdin.buffer.read())
# print("Content-type: application/octet-stream\r\n\r\n")
# sys.exit()

# import sys
# import email.parser

# input_data = sys.stdin.buffer.read()
# with open("data", "wb") as f:
#     # f.write(input_data)
#     msg = email.parser.BytesParser().parsebytes(input_data)
#     f.write(str.encode("payload type: {}\n".format(type(msg.get_payload()))))
#     f.write(str.encode("decoded payload len: {}\n".format(len(msg.get_payload(decode=True)))))
#     f.write(str.encode("payload len: {}\n".format(len(msg.get_payload()))))
#     f.write(str.encode("multipart: {}\n".format((msg.is_multipart()))))
#     f.write(str.encode("payload:\n{}".format(msg.get_payload())))
#     #f.write(str.encode("raw input data:\n{}".format(input_data))
#     # print({
#     #     part.get_param('name', header='content-disposition'): part.get_payload(decode=True)
#     #     for part in msg.get_payload()
#     # })

# Import modules for CGI handling
import cgi, cgitb
import sys
# import cgitb; cgitb.enable()

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get data from fields
name = form.getvalue('name')
story = form.getvalue('story')

with open("log", "wb") as f:
    f.write("{}".format(form.keys()).encode('utf-8'))
    # fileitem = form.getvalue('file')
    # if fileitem.filename:
    #     f.write(fileitem.filename)
    # else:
    #     f.write(b'No file was uploaded')

with open("data2", "wb") as f:
    # f.write(input_data)
    # msg = email.parser.BytesParser().parsebytes(input_dat
    f.write(str.encode("NAME: {}<br/>\n".format(name)))
    f.write(str.encode("STORY: {}\n".format(story)))


print("Content-type: application/octet-stream\r\n\r\n")
