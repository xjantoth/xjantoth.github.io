---
title: "How to Cut a Portion of a Video"
date: "2022-01-07T11:20:28+0100"
lastmod: "2022-01-07T11:20:28+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Use ffmpeg to extract a specific time segment from a video file with a single command."

tags: ['cut', 'portion', 'video']
categories: ["DevOps"]
---

## Trim a video with ffmpeg

The following `ffmpeg` command extracts a portion of a video. The `-ss` flag sets the start time and `-t` sets the duration (or end time). Replace `<input-file>` and `<output-file>` with your actual filenames.

```bash
ffmpeg \
-t 4:12 \
-i <input-file>.mp4 \
-ss 4:07  \
<output-file>.mp4
```
