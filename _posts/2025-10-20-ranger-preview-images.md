---
title: "Ranger preview images"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Https://unix.stackexchange.com/questions/632529/alacritty-ranger-w3m-images-are-not-showing-or-disappear-after-few-seconds?newreg=05e6c4f5bf2345e48c22340fd7bee222."
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
tags: ['ranger', 'preview', 'images']
categories: ["DevOps"]
---

https://unix.stackexchange.com/questions/632529/alacritty-ranger-w3m-images-are-not-showing-or-disappear-after-few-seconds?newreg=05e6c4f5bf2345e48c22340fd7bee222

```
I got it working with ueberzug, even inside tmux

set preview_images true
set use_preview_script true
set preview_images_method ueberzug


yay -S  alacritty
sudo pacman -S ueberzug
```
