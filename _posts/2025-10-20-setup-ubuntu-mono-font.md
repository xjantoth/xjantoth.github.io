---
title: "Setup Ubuntu Mono font"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to install the Ubuntu Mono font on Arch Linux and configure it in the Alacritty terminal emulator."

image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
tags: ['setup', 'ubuntu', 'mono', 'font']
categories: ["DevOps"]
---

Install the Ubuntu font family using the AUR helper `yay`, then enable LCD font filtering and sub-pixel rendering by creating the appropriate symlinks.

```bash
yay -S ttf-ubuntu-font-family

ln -s /usr/share/fontconfig/conf.avail/11-lcdfilter-default.conf /etc/fonts/conf.d/
ln -s /usr/share/fontconfig/conf.avail/10-sub-pixel-rgb.conf /etc/fonts/conf.d/
```

## Setup Alacritty

To use Ubuntu Mono in the Alacritty terminal, update the font family in its configuration file as shown below.

```yaml
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
