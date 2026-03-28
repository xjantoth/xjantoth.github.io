---
title: "Pacman setup mirrors and refresh keys"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to refresh Arch Linux pacman GPG keys and configure the fastest package mirrors using reflector."

image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
tags: ['pacman', 'setup', 'mirrors', 'refresh', 'keys']
categories: ["DevOps"]
---

These commands refresh the pacman keyring (useful when encountering signature verification errors) and then use `reflector` to automatically find and save the fastest HTTPS mirrors from nearby countries. Run these after a fresh Arch Linux install or when mirrors become stale.

```bash
# refresh gpg keys if needed
sudo pacman-key --refresh-keys
sudo pacman-key --populate archlinux

# setup closest mirrors
reflector --country Slovakia --country Czechia --protocol https --age 12 --sort rate --save
```
