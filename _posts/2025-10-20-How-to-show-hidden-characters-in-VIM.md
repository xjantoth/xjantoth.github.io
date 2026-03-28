---
title: "Vim show hidden characters"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "How to display hidden characters such as tabs, trailing spaces, and line endings in Vim using the listchars option."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"

tags: ['vim', 'hidden', 'characters']
categories: ["Linux"]
---

To reveal invisible characters in Vim, use the `:set listchars` command. This configures how each type of hidden character is displayed: `$` for end-of-line, `>-` for tabs, `~` for trailing spaces, and angle brackets for text extending beyond the visible area. After setting this, enable it with `:set list`.

```vim
:set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<
```
