#!/usr/bin/env python

import glob
import re
import ast

all_files = glob.glob("_posts/*.md")
remove = relevant_words = [
    "apply", "install", "protect", "push", "work", "backup", "generate",
    "replace", "remove", "verify", "upload", "installing", "serving",
    "delete", "attack", "connect", "manage", "create", "keep", "find",
    "test", "run", "sort", "use", "restrict", "reduce", "analyze", "write",
    "and", "or", "else", "while", "if", "but",
    "from", "how", "at", "on", "to", "by", "in", "via", "with", "for", "of"
]

all_tags = []
for x, _file in enumerate(all_files):
  with open(_file, 'r', encoding='utf-8') as file:
      c = file.readlines()

      for e, line in enumerate(c):
        if line.startswith("tags:"):
          # line = True
          if re.search(r'^tags:.*', line):
            s = line.split(":")[1].strip(" ")
            l = ast.literal_eval(s)
            all_tags += l
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
              if re.search(r"-", i):
                # print(f"delefing: {i}")
                l.remove(i)
              for _remove in remove:
                if i == _remove:
                  l.remove(i)

            c[e] = f"tags: {l}\n"
# print(set(all_tags), len(set(all_tags)))



  with open(_file, 'w', encoding='utf-8') as file:
      for line in c:
          file.write(line)  # Add a newline to each line

