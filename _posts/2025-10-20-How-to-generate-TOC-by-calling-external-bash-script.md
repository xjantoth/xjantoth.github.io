---
title: "How to generate TOC by calling external sh"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "How to generate TOC by calling external sh"
image: "/assets/images/blog/vim-1.jpg"

tags: ['vim', 'generate', 'toc']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
