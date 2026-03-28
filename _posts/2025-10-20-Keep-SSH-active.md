---
title: "Keep SSH active"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "Prevent SSH connections from timing out by configuring a keep-alive interval in your SSH config file."

tags: ['ssh', 'active']
categories: ["Networking"]
---

**Make this part of your SSH config file.**

Add the following to your `~/.ssh/config` to send keep-alive packets every 60 seconds, preventing idle SSH sessions from being dropped by firewalls or NAT devices. The `AddressFamily inet` directive forces IPv4 connections.

```bash
worker ~ $ cat ~/.ssh/config
Host *
    ServerAliveInterval 60
    AddressFamily inet

```
