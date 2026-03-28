---
title: "Concat mp4 file with ffmpeg"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to concatenate multiple MP4 video files using ffmpeg with a text-based file list and a bash loop."

tags: ['concat', 'mp4', 'file', 'ffmpeg']
categories: ["DevOps"]
---

Concatenate video files (e.g. MP4) specified in a text file using ffmpeg's concat demuxer.

Example: If you have MP4 files numbered from 1 to 46, each text file references a sound intro, the rendered segment, and a sound outro.

```text
file sound.mp4
file 46-Con-xyz-rendered.mp4
file sound.mp4
```

This loop iterates over all 46 files, generates a text file listing the sound and rendered segments, and uses `ffmpeg -f concat` to concatenate them into a final MP4 file.

```bash
for i in {1..46}; do
    file=$(echo ${i}-*-rendered.mp4);
    touch ${file};
    echo -e "file sound.mp4\nfile ${file}\nfile sound.mp4" > ${file%.mp4}.txt;
    ffmpeg -f concat -safe 0 -i ${file%.mp4}.txt -c copy ${file%.mp4}-final.mp4;
done
```
