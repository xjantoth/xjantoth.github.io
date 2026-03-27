---
title: "Determine the length of mp4 file"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Determine the length of mp4 file — practical walkthrough with examples."

tags: ['determine', 'the', 'length', 'mp4', 'file']
categories: ["DevOps"]
---

```
for i in file1.mp4 file2.mp4 file3.mp4   ; do
    t=$(ffmpeg -i $i  2>&1 | grep Duration | awk '{print $2}' | tr -d ,);
    echo " $t: $i";
done
```
