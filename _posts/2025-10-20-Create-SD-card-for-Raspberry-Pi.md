---
title: "Create SD card for Raspberry Pi"
date: "2021-12-30T16:09:28+0100"
lastmod: "2021-12-30T16:09:28+0100"
draft: false
author: "Jan Toth"
description: "Create SD card for Raspberry Pi"
image: "/assets/images/blog/raspberrypi/raspberrypi.png"

tags: ["raspberry", "sd", "card"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```

lsblk -p
NAME                      MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
/dev/mmcblk0              179:0    0  14.5G  0 disk
/dev/nvme0n1              259:0    0 476.9G  0 disk
├─/dev/nvme0n1p1          259:1    0   360M  0 part  /boot/efi
├─/dev/nvme0n1p2          259:2    0 237.8G  0 part
├─/dev/nvme0n1p3          259:3    0 237.8G  0 part
│ └─/dev/mapper/archlinux 254:0    0 237.8G  0 crypt /
└─/dev/nvme0n1p6          259:4    0     1G  0 part  /boot


unzip -p ~/Downloads/2020-05-27-raspios-buster-full-armhf.zip | sudo dd of=/dev/mmcblk0 bs=4M conv=fsync
```
