---
title: "VPN in Archlinux"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to install the required VPN packages on Arch Linux using pacman for OpenConnect-based VPN connections."

image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
tags: ['vpn', 'archlinux']
categories: ["Networking"]
---

Install the necessary packages for OpenConnect VPN on Arch Linux. This includes the NetworkManager plugin for OpenConnect, the OpenConnect client itself, and OpenSSL.

```bash
sudo pacman -S  networkmanager-openconnect openconnect openssl
```
