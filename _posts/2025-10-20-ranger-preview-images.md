---
title: "Ranger preview images"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Fix image previews in Ranger file manager on Alacritty terminal by using ueberzug instead of w3m."
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
tags: ['ranger', 'preview', 'images']
categories: ["DevOps"]
---

Reference: [Alacritty ranger w3m images fix](https://unix.stackexchange.com/questions/632529/alacritty-ranger-w3m-images-are-not-showing-or-disappear-after-few-seconds)

If image previews in Ranger disappear after a few seconds or do not show at all when using Alacritty, switch the preview method from w3m to ueberzug. Add the following settings to your Ranger `rc.conf` and install the required packages.

```bash
# Ranger rc.conf settings
set preview_images true
set use_preview_script true
set preview_images_method ueberzug

# Install required packages on Arch Linux
yay -S  alacritty
sudo pacman -S ueberzug
```
