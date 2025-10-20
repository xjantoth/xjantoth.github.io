---
title: "Ranger preview images"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Ranger preview images"
image: "/assets/images/blog/linux-1.jpg"
tags: ['ranger', 'preview', 'images']
categories: ["tiddlywiki"]

hiddenFromSearch: false
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
