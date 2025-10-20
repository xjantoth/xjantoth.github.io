---
title: "Delete database entries via bash alias"
date: "2022-01-07T11:20:36+0100"
lastmod: "2022-01-07T11:20:36+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "Delete database entries via bash alias"

tags: ['delete', 'database', 'entries', 'via', 'bash', 'alias']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
alias delprn='psql "host=127.0.0.1 port=5432 sslmode=disable user=rednetwork password=password" <<< "delete from port_range_networks where id between 1 and 10000;"'
```
