---
title: "newman open html reports"
date: "2022-01-07T11:20:36+0100"
lastmod: "2022-01-07T11:20:36+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "newman open html reports"

tags: ['newman', 'open', 'html', 'reports']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
open "$(greadlink -f  "$(ls -tr newman/* | tail -n 1 )")"
```
