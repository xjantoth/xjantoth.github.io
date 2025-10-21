---
title: "Determine the length of mp4 file"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "Determine the length of mp4 file"

tags: ['determine', 'the', 'length', 'mp4', 'file']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
for i in file1.mp4 file2.mp4 file3.mp4   ; do
    t=$(ffmpeg -i $i  2>&1 | grep Duration | awk '{print $2}' | tr -d ,);
    echo " $t: $i";
done
```
