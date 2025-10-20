#!/usr/bin/env python

import glob
import re
import ast

all_files = glob.glob("_posts/*.md")

for x, _file in enumerate(all_files):
  with open(_file, 'r', encoding='utf-8') as file:
      c = file.readlines()

      for e, line in enumerate(c):
        if line.startswith("tags:"):
          # line = True
          if re.search(r'^tags:.*', line):
            s = line.split(":")[1].strip(" ")
            l = ast.literal_eval(s)
            for i in l:
              if re.match(r'\d+', i):
                # print(f"delefing: {i}")
                l.remove(i)
              if re.search(r"\(.*\)", i):
                # print(f"delefing: {i}")
                l.remove(i)
              if re.search(r"<title><title>", i):
                # print(f"delefing: {i}")
                l.remove(i)
            print(l)

            c[e] = f"tags: {l}\n"




  with open(_file, 'w', encoding='utf-8') as file:
      for line in c:
          file.write(line)  # Add a newline to each line

