---
title: "How to generate TOC by calling external sh"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "Practical guide on how to generate a table of contents by calling an external bash script from within Vim."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"

tags: ['vim', 'toc']
categories: ["Linux"]
---

This bash script extracts HTML comment markers from a file and strips the comment delimiters, producing a table of contents based on specially formatted comments in your README or documentation files.

```bash
 cat ~/bin/tocreadme.sh
#!/bin/bash

grep "<\!--" $1 | sed -E 's/^(<!--)(.*)(-->)/\2/'

```

To use this script from within Vim, add a key mapping to your `.vimrc` that calls the external script and inserts its output at the cursor position.

```vim
cat ~/.vimrc

...
nmap <leader>c :read! sh tocreadme.sh ~/Documents/sbx/aws-eks-devopsinuse/README.md <CR>

...
:wq!
```
