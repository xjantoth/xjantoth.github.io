---
title: "Pacman setup mirrors and refresh keys"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Pacman setup mirrors and refresh keys"

image: "/assets/images/blog/linux-1.jpg"
tags: ['pacman', 'setup', 'mirrors', 'and', 'refresh', 'keys']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
# refresh gpg keys if needed
sudo pacman-key --refresh-keys
sudo pacman-key --populate archlinux

# setup closest mirrors
reflector --country Slovakia --country Czechia --protocol https --age 12 --sort rate --save
```
