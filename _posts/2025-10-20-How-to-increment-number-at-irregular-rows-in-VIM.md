---
title: "Vim increment number at irregular rows"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "Vim increment number at irregular rows — practical walkthrough with examples."
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"

tags: ['vim', 'increment', 'rows']
categories: ["Linux"]
---

Suppose you have a JSON structure with repeated `_iteration` fields that all have the same value (e.g. `0`), and you need to renumber them sequentially. Here is the initial state:

```json
[{
    "payload": {
        "data": {
            "vlan_id": 27,
            ...
        }
    },
    "_response": 200,
    ...
    "_iteration": 0           <---
}, {
    "payload": {
        "data": {
            "vlan_id": 27,
       ...
        }
    },
    "_response": 400,
    ...
    "_iteration": 0.         <---

```

The following Vim command uses `:g` (global) to find every line containing `_iteration`, then substitutes the first number on that line with an auto-incrementing counter. The variable `c` starts at 1 and increases by 1 after each replacement.

```vim
:let c=1 | g/_iteration/ s/\d\+/\=c/ | let c+=1
```

**Result**

After running the command, every `_iteration` value is replaced with a unique sequential number:

```json
[{
    "payload": {
        "data": {
            "vlan_id": 27,
            ...
        }
    },
    "_response": 200,
    ...
    "_iteration": 1
}, {
    "payload": {
        "data": {
            "vlan_id": 27,
       ...
        }
    },
    "_response": 400,
    ...
    "_iteration": 2

...

```
