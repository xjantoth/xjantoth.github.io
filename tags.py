#!/usr/bin/env python

import glob
import os
import re
import sys
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')

# Check if the filename is provided
# if len(sys.argv) < 2:
#     print("Usage: python script.py <filename>")
#     sys.exit(1)
#
# f = sys.argv[1]

all_files = glob.glob("_posts/*.md")

for _file in all_files:
  with open(_file, 'r', encoding='utf-8') as file:
      c = file.readlines()

      for e, line in enumerate(c):
        if line.startswith("tags:"):
          # line = True
          if re.search(r'^tags:.*', line):
            # print(_file, line)
            print(line)



          # c[e] = f"tags: {title}\n".strip("\"")




      # with open(f"{p}/{current_date}-{fn}", 'w', encoding='utf-8') as file:
      #     for line in c:
      #         file.write(line)  # Add a newline to each line

