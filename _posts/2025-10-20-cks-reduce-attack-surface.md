---
title: "CKS Reduce Attack Surface"
date: 2022-06-12T20:58:37+0200
lastmod: 2022-06-12T20:58:37+0200
draft: false
description: "CKS Reduce Attack Surface"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'reduce', 'attack', 'surface']
---

##### Overview

* only purpose (remove unneceassary services)
* node recycling (should be ephemeral, created from images)
* ubuntu, centos

![Image](/assets/images/blog/aa-1.png)



```
systemctl list-units | grep <service-name>
systemctl list-units --type=service | grep <service-name>
systemctl list-units --type=service --state=running | grep <service-name>



```
