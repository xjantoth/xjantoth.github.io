---
title: "Install Ubuntu 20.04 (Raspberry Pi 3)"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=800&h=420&fit=crop"
description: "Step-by-step guide to installing Ubuntu 20.04 on a Raspberry Pi 3, including Wi-Fi setup, SSH access, and initial password change."

tags: ['ml', 'ubuntu', 'raspberry']
categories: ["Raspberry Pi"]
---

##  Install Ubuntu on Raspberry Pi 3

This command decompresses the Ubuntu image and writes it directly to the SD card. Make sure `/dev/mmcblk0` is your SD card device before running this.

```bash
xz --decompress --stdout ~/Downloads/ubuntu-20.04.1-preinstalled-server-arm64+raspi.img.xz | sudo dd of=/dev/mmcblk0 bs=4M conv=fsync status=progress

```


##  Ubuntu on Raspberry Pi Wi-Fi setup

Edit the `network-config` file in the system-boot partition to configure Wi-Fi. Ubuntu uses Netplan syntax for network configuration. Replace the SSID and password with your own values.

```yaml
vim  /run/media/jantoth/system-boot/network-config
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

Creating an empty `ssh` file in the system-boot partition enables the SSH server on first boot for headless access.

```bash
touch  /run/media/jantoth/system-boot/ssh
```

##  First SSH to Ubuntu on Raspberry Pi

Use `arp` to find the Raspberry Pi on your local network. The MAC address prefix `b8:27:eb` is specific to Raspberry Pi 3 devices.

```bash
arp -na | grep -i "b8:27:eb"
? (192.168.1.196) at b8:27:eb:87:e6:c5 [ether] on wlp1s0

 ping 192.168.1.196
PING 192.168.1.196 (192.168.1.196) 56(84) bytes of data.
64 bytes from 192.168.1.196: icmp_seq=1 ttl=64 time=279 ms
64 bytes from 192.168.1.196: icmp_seq=2 ttl=64 time=3.25 ms
64 bytes from 192.168.1.196: icmp_seq=3 ttl=64 time=3.01 ms

```


##  Change initial password

On first SSH login, Ubuntu requires you to change the default password. The default username and password are both `ubuntu`.

```bash
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
