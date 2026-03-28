---
title: "Determine the length of mp4 file"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "A short bash loop using ffmpeg to determine the duration of multiple MP4 files."

tags: ['determine', 'the', 'length', 'mp4', 'file']
categories: ["DevOps"]
---

This bash one-liner loops through a list of MP4 files and uses `ffmpeg` to extract the duration of each file. The `grep`, `awk`, and `tr` pipeline parses the duration value from ffmpeg's stderr output.

```bash
for i in file1.mp4 file2.mp4 file3.mp4   ; do
    t=$(ffmpeg -i $i  2>&1 | grep Duration | awk '{print $2}' | tr -d ,);
    echo " $t: $i";
done
```
