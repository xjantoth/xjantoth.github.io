---
title: "Concat mp4 file with ffmpeg"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "Concat mp4 file with ffmpeg"

tags: ['concat', 'mp4', 'file', 'ffmpeg']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Concatenated'' video files (e.g. *.mp4) specified in *.txt file ''created'' on the file

Example: If you got *.mp4 files starting from: 1 to 46


```
file sound.mp4
file 46-Con-xyz-rendered.mp4
file sound.mp4
```


```
for i in {1..46}; do
    file=$(echo ${i}-*-rendered.mp4);
    touch ${file};
    echo -e "file sound.mp4\nfile ${file}\nfile sound.mp4" > ${file%.mp4}.txt;
    ffmpeg -f concat -safe 0 -i ${file%.mp4}.txt -c copy ${file%.mp4}-final.mp4;
done
```
