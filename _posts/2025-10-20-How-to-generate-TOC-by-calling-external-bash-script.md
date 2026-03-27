---
title: "How to generate TOC by calling external sh"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "Practical guide: how to generate TOC by calling external sh."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"

tags: ['vim', 'toc']
categories: ["Linux"]
---

```
 cat ~/bin/tocreadme.sh
#!/bin/bash

grep "<\!--" $1 | sed -E 's/^(<!--)(.*)(-->)/\2/'

```


```vim
cat ~/.vimrc

...
nmap <leader>c :read! sh tocreadme.sh ~/Documents/sbx/aws-eks-devopsinuse/README.md <CR>

...
:wq!
```
