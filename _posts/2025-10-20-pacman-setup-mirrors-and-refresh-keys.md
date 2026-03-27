---
title: "Pacman setup mirrors and refresh keys"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Pacman setup mirrors and refresh keys — practical walkthrough with examples."

image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
tags: ['pacman', 'setup', 'mirrors', 'refresh', 'keys']
categories: ["DevOps"]
---

```
# refresh gpg keys if needed
sudo pacman-key --refresh-keys
sudo pacman-key --populate archlinux

# setup closest mirrors
reflector --country Slovakia --country Czechia --protocol https --age 12 --sort rate --save
```
