---
title: "Delete database entries via bash alias"
date: "2022-01-07T11:20:36+0100"
lastmod: "2022-01-07T11:20:36+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=800&h=420&fit=crop"
description: "Delete database entries via bash alias — practical walkthrough with examples."

tags: ['database', 'entries', 'bash', 'alias']
categories: ["Linux"]
---

```
alias delprn='psql "host=127.0.0.1 port=5432 sslmode=disable user=rednetwork password=password" <<< "delete from port_range_networks where id between 1 and 10000;"'
```
