---
title: "How to cut a portion of video"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Practical guide: how to cut a portion of video."

tags: ['cut', 'portion', 'video']
categories: ["DevOps"]
---

```
ffmpeg \
-t 4:12 \
-i <input-file>.mp4 \
-ss 4:07  \
<output-file>.mp4
```
