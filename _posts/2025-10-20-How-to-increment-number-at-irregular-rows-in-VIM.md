---
title: "Vim increment number at irregular rows"
date: "2021-12-31T16:18:38+0100"
lastmod: "2021-12-31T16:18:38+0100"
draft: false
author: "Jan Toth"
description: "vim increment number at irregular rows"
image: "/assets/images/blog/vim-1.jpg"

tags: ["vim", "increment", "rows"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
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


```
:let c=1 | g/_iteration/ s/\d\+/\=c/ | let c+=1
```

**Result''

```
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
