#!/usr/bin/env python

import os
import re
import sys
from datetime import datetime

current_date = datetime.now().strftime('%Y-%m-%d')

# Check if the filename is provided
if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    sys.exit(1)

f = sys.argv[1]

with open(f, 'r', encoding='utf-8') as file:
    c = file.readlines()


title = []
for e, line in enumerate(c):
  if line.startswith("title:"):
    line = line.strip("()-[]").replace("\"", "").split(":")[1].strip(" ") # remove brackets
    title = [word.lower() for word in line.split()]

# rewrite tags
for e, line in enumerate(c):
  if line.startswith("tags:"):
    c[e] = f"tags: {title}\n".strip("\"")


for e, line in enumerate(c):
  if line.startswith("image:"):
    c[e] = re.sub(r'^(image:\s*")([^/])', r'image: "/assets/\2', line)



# print(c)

p, fn = f.split("/")


with open(f"{p}/{current_date}-{fn}", 'w', encoding='utf-8') as file:
    for line in c:
        file.write(line)  # Add a newline to each line


os.remove(f)



# for i in  "_posts/Connecting-to-PostgreSQL-via-Cloud-SQL-Proxy.md" "_posts/Google-cloud-pipeline-example.md"; do
#   ./adjust.py $i
# done

