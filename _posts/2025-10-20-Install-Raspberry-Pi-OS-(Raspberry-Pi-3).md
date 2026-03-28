---
title: "Install Raspberry Pi OS (Raspberry Pi 3)"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "Guide to installing Raspberry Pi OS on a Raspberry Pi 3, including SD card flashing, Wi-Fi configuration, and SSH setup."

tags: ['ml', 'raspberry', 'k3s', 'os']
categories: ["Kubernetes"]
---

https://www.raspberrypi.org/documentation/installation/installing-images/linux.md

##  Check SD card presence at your laptop

Use `lsblk -p` to verify that the SD card is detected by the system. Look for a device like `/dev/mmcblk0` in the output.

```bash
lsblk -p
NAME                      MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
/dev/sda                    8:0    0     1G  0 disk  /var/lib/kubelet/pods/d6fe24f2-3dc7-4291-90f5-8c7dbb4e8382/volu
/dev/mmcblk0              179:0    0  14.8G  0 disk
├─/dev/mmcblk0p1          179:1    0   256M  0 part
└─/dev/mmcblk0p2          179:2    0  14.6G  0 part
/dev/nvme0n1              259:0    0 476.9G  0 disk
├─/dev/nvme0n1p1          259:1    0   360M  0 part  /boot/efi
├─/dev/nvme0n1p2          259:2    0 237.8G  0 part
├─/dev/nvme0n1p3          259:3    0 237.8G  0 part
│ └─/dev/mapper/archlinux 254:0    0 237.8G  0 crypt /
└─/dev/nvme0n1p6          259:4    0     1G  0 part  /boot
```

##  Install Raspbian on Raspberry Pi 3

This command unzips the Raspberry Pi OS image and writes it directly to the SD card using `dd`. Make sure the target device (`/dev/mmcblk0`) matches your SD card.

```bash
unzip -p ~/Downloads/2020-08-20-raspios-buster-armhf-lite-correct.zip| sudo dd of=/dev/mmcblk0 bs=4M conv=fsync status=progress
```

##  WPA supplicant Raspberry Pi OS

https://www.raspberrypi.org/documentation/configuration/wireless/headless.md

**wpa_supplicant.conf** file example:

Place a `wpa_supplicant.conf` file in the boot partition to enable headless Wi-Fi configuration. Replace the country code, SSID, and password with your own values.

```ini
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=<Insert 2 letter ISO 3166-1 country code here>

network={
 ssid="<Name of your wireless LAN>"
 psk="<Password for your wireless LAN>"
}
```

After flashing the image, verify that the SD card partitions are now visible. The boot partition should be mounted automatically.

```bash
lsblk -p
NAME                      MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
/dev/sda                    8:0    0     1G  0 disk  /var/lib/kubelet/pods/d6fe24f2-3dc7-4291-90f5-8c7dbb4e8382/volu
/dev/mmcblk0              179:0    0  14.8G  0 disk
├─/dev/mmcblk0p1          179:1    0   256M  0 part  /run/media/jantoth/boot
└─/dev/mmcblk0p2          179:2    0   1.5G  0 part
/dev/nvme0n1              259:0    0 476.9G  0 disk
├─/dev/nvme0n1p1          259:1    0   360M  0 part  /boot/efi
├─/dev/nvme0n1p2          259:2    0 237.8G  0 part
├─/dev/nvme0n1p3          259:3    0 237.8G  0 part
│ └─/dev/mapper/archlinux 254:0    0 237.8G  0 crypt /
└─/dev/nvme0n1p6          259:4    0     1G  0 part  /boot
```

##  Create an empty ssh file

Creating an empty file named `ssh` in the boot partition enables the SSH server on first boot, which is essential for headless setups.

```bash
touch /run/media/jantoth/boot/ssh
```

##  Create wpa_supplicant.conf in the boot partition

Edit or create `/run/media/jantoth/boot/wpa_supplicant.conf` with your actual Wi-Fi credentials. This file will be picked up on first boot.

```ini
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=SK

network={
 ssid="ASUS"
 psk="potrubie"
}
```
