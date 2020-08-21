#!/usr/bin/python3                                                      
                                                                        
import datetime                                                         
import os                                                               
import json   
       
d = {"now": str(datetime.datetime.now())}
d.update(dict(os.environ))
print("Content-type: application/json\r\n\r\n", end="")                       
print(json.dumps(d, indent = 4))
