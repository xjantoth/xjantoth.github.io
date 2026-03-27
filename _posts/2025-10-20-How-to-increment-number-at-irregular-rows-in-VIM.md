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
