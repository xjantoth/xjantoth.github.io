---
title: "How to server Jekkyl from github pages"
date: 2025-10-20T11:46:24:+0200
lastmod: 2025-10-20T11:46:24:+0200
draft: false
description: "How to server Jekkyl from github pages"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['websupport', 'jekkyl']
---

How to set custom domain at Github pages at Websupport.

- set 4 A-recors
- one CNAME www.<domain>.com

![Image](/assets/images/blog/ws-1.png)

![Image](/assets/images/blog/ws-2.png)


## Upgrade and keep up with changes

https://github.com/cotes2020/jekyll-theme-chirpy/wiki/Upgrade-Guide

```bash
git remote add chirpy https://github.com/cotes2020/chirpy-starter.git
git checkout -b upgrade/v7.4.0
git restore --staged assets/lib
git checkout --ours _config.yml

```
