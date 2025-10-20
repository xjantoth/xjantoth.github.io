---
title: "Setup Ubuntu Mono font"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Setup Ubuntu Mono font"

image: "/assets/images/blog/linux-1.jpg"
tags: ['setup', 'ubuntu', 'mono', 'font']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
yay -S ttf-ubuntu-font-family

ln -s /usr/share/fontconfig/conf.avail/11-lcdfilter-default.conf /etc/fonts/conf.d/
ln -s /usr/share/fontconfig/conf.avail/10-sub-pixel-rgb.conf /etc/fonts/conf.d/
```

**Setup Alacrity''

```
104 # Font configuration
  1 font:
  2   # Normal (roman) font face
  3   normal:
  4     # Font family
  5     #
  6     # Default:
  7     #   - (macOS) Menlo
  8     #   - (Linux/BSD) monospace
  9     #   - (Windows) Consolas
 10     family: Ubuntu Mono
 ```
