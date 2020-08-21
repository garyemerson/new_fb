#!/usr/bin/python3

import random

s = "hello"
colors = ["#%06x" % random.randrange(0xffffff) for _ in range(len(s))]
ch_clrs = list(zip(s, colors))
spans = "".join("<span style=\"color: {};\">{}</span>".format(clr, ch) for ch, clr in ch_clrs)
print("<h1>{}</h1>".format(spans))
