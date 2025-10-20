---
title: "How to cut a portion of video"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "How to cut a portion of video"

tags: ['how', 'to', 'cut', 'a', 'portion', 'of', 'video']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
ffmpeg \
-t 4:12 \
-i <input-file>.mp4 \
-ss 4:07  \
<output-file>.mp4
```
