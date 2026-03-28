---
title: "How to serve Jekyll from GitHub Pages"
date: 2025-10-20T11:46:24:+0200
lastmod: 2025-10-20T11:46:24:+0200
draft: false
description: "How to set custom domain at Github pages at Websupport. Template repo was created from https://github.com/cotes2020/chirpy-starter."
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['websupport', 'jekyll']
categories: ["DevOps"]
---

How to set custom domain at Github pages at Websupport.
Template repo was created from https://github.com/cotes2020/chirpy-starter

- set 4 A-records
- one CNAME www.<domain>.com

![Image](/assets/images/blog/ws-1.png)

![Image](/assets/images/blog/ws-2.png)


## Upgrade and keep up with changes

Follow the [Chirpy Upgrade Guide](https://github.com/cotes2020/jekyll-theme-chirpy/wiki/Upgrade-Guide) to stay current with theme updates. The commands below add the upstream starter as a remote, create an upgrade branch, resolve conflicts, and update bundled dependencies.

```bash
git remote add chirpy https://github.com/cotes2020/chirpy-starter.git
git checkout -b upgrade/v7.4.0
git restore --staged assets/lib
git checkout --ours _config.yml
git add .
git commit -m "upgrade theme to v7.4.0"
bundle update
git push 

```
