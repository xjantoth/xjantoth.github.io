---
title: How to use bufdo in Neovim
date: 2024-03-26T13:19:22+0100
lastmod: 2024-03-26T13:19:22+0100
description: "How to use Neovim bufdo command to perform bulk edits across multiple YAML files matching a glob pattern."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'vim', 'nvim', 'bufdo']
categories: ["Linux"]
---

- Find all YAML files that satisfy a pattern, open them in Vim and delete each line that contains a specific string.

The `:bufdo` command runs an Ex command across all open buffers. Combined with `:g/pattern/d`, it deletes every matching line in every file. The `| update` part saves each buffer after the deletion. This is a fast way to bulk-remove lines from many files at once without leaving Vim.

```vim
v organization/*/*/*/*/XZY*.yaml
:bufdo exe "g/bigtable.googleapis.com/d" | update
```


