---
title: "Install Ubuntu 20.04 (Raspberry Pi 4 8GB)"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Install Ubuntu 20.04 (Raspberry Pi 4 8GB)"

tags: ["ml", "install", "ubuntu", "raspberry"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  1. Install Ubuntu at Raspberry Pi 3

```
xz --decompress --stdout ~/Downloads/ubuntu-20.04.1-preinstalled-server-arm64+raspi.img.xz | sudo dd of=/dev/mmcblk0 bs=4M conv=fsync status=progress

```

##  2. Click at ''upper left corner and mount SD card'' in your Archlinux/Windows/MAC

##  3. Ubuntu at Raspberry Pi WIFI setup

```
vim  /run/media/jantoth/system-boot/network-config
...
version: 2
ethernets:
  eth0:
    dhcp4: true
    optional: true
wifis:
  wlan0:
    dhcp4: true
    optional: true
    access-points:
      "ASUS":
        password: "potrubie"

~
```

##  Create an empty ssh file in system-boot folder

```
touch  /run/media/jantoth/system-boot/ssh
```

##  First SSH to Ubuntu at Raspberry Pi

```
arp -na | grep -i "b8:27:eb"
? (192.168.1.196) at b8:27:eb:87:e6:c5 [ether] on wlp1s0

 ping 192.168.1.196
PING 192.168.1.196 (192.168.1.196) 56(84) bytes of data.
64 bytes from 192.168.1.196: icmp_seq=1 ttl=64 time=279 ms
64 bytes from 192.168.1.196: icmp_seq=2 ttl=64 time=3.25 ms
64 bytes from 192.168.1.196: icmp_seq=3 ttl=64 time=3.01 ms

```


##  Change initial password (9c3f5f7f00c25e7839b118425d7a81363f15cd21d222a93205ff6bea408ca792)

```
 ssh ubuntu@k3s-rpi-1
ubuntu@k3s-rpi-1's password:
You are required to change your password immediately (administrator enforced)
Welcome to Ubuntu 20.04.1 LTS (GNU/Linux 5.4.0-1015-raspi aarch64)
...
...
WARNING: Your password has expired.
You must change your password now and login again!
Changing password for ubuntu.
Current password:
New password:
Retype new password:
passwd: password updated successfully
Connection to k3s-rpi-1 closed.

```
