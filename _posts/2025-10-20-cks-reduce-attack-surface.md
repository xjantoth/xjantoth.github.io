---
title: "CKS Reduce Attack Surface"
date: 2022-06-12T20:58:37+0200
lastmod: 2022-06-12T20:58:37+0200
draft: false
description: "CKS exam topic: Reduce Attack Surface — concepts, configuration, and practice exercises."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'attack', 'surface']
categories: ["Kubernetes"]
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
