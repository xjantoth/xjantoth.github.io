---
title: How to use bufdo in Neovim
date: 2024-03-26T13:19:22+0100
lastmod: 2024-03-26T13:19:22+0100
description: "Find all yaml files that satisfy pattern, open them in Vim and delete each line that has some string in it."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'vim', 'nvim', 'bufdo']
categories: ["Linux"]
---

- Find all yaml files that satisfy pattern, open them in Vim and delete each line that has some string in it

```
v organization/*/*/*/*/XZY*.yaml
:bufdo exe "g/bigtable.googleapis.com/d" | update
```


## Links:

202403261303
