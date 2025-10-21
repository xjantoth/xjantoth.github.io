---
title: "How to use cryptsetup while installing archlinux"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "cryptsetup"

image: "/assets/images/blog/linux-1.jpg"
tags: ['to', 'cryptsetup', 'installing', 'archlinux']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

Kriskoviny

```
# boot arch iso and set root passwd
passwd
systemctl start sshd
ssh -l root 192.168.1.225
ping archlinux.org
timedatectl set-ntp true
date
cfdisk /dev/sda
# sda1 450MB EFI
# sda2 450MB Linux
# sda3 rest  Linux
cryptsetup luksFormat --type luks1 /dev/sda2
cryptsetup open /dev/sda2 boot
cryptsetup luksFormat /dev/sda3
cryptsetup open /dev/sda3 system
mkfs.fat -F32 /dev/sda1
mkfs.btrfs -L boot /dev/mapper/boot
mkfs.btrfs -L system /dev/mapper/system
vim /etc/pacman.d/mirrorlist
mkdir /mnt/{subvolumes,arch-chroot}
mount /dev/mapper/system /mnt/subvolumes
btrfs subvolume create /mnt/subvolumes/home
btrfs subvolume create /mnt/subvolumes/root
mount -o subvol=root /dev/mapper/system /mnt/arch-chroot
mkdir /mnt/arch-chroot/{home,boot,efi}
mount -o subvol=home /dev/mapper/system /mnt/arch-chroot/home
mount /dev/mapper/boot /mnt/arch-chroot/boot
mount /dev/sda1 /mnt/arch-chroot/efi
pacstrap /mnt/arch-chroot base vim openssh btrfs-progs base-devel refind-efi intel-ucode grub grub-btrfs efibootmgr linux linux-firmware mkinitcpio dhcpcd dhclient wpa_supplicant netctl
genfstab -U /mnt/arch-chroot >> /mnt/arch-chroot/etc/fstab
arch-chroot /mnt/arch-chroot
ln -sf /usr/share/zoneinfo/Europe/Bratislava /etc/localtime
hwclock --systohc
date
cat <<EOF >>/etc/locale.gen
en_US.UTF-8 UTF-8
en_US ISO-8859-1
sk_SK.UTF-8 UTF-8
sk_SK ISO-8859-2
EOF
locale-gen
cat <<EOF >>~/.vimrc
set mouse-=a
EOF
cat <<EOF >/etc/locale.conf
LANG=en_US.UTF-8
EOF
cat <<EOF >/etc/hostname
archvbox
EOF
cat <<EOF >>/etc/hosts
127.0.0.1       localhost
127.0.0.1       archvbox.localdomain archvbox
EOF
vim /etc/mkinitcpio.conf
# HOOKS=(base udev autodetect keyboard keymap modconf block encrypt filesystems fsck)
mkinitcpio -p linux
passwd
# uncomment in /etc/default/grub
GRUB_ENABLE_CRYPTODISK=y
# add to GRUB_CMDLINE_LINUX_DEFAULT
cryptdevice=UUID=</dev/sda3 UUID from /dev/disk/by-uuid>:system
grub-install --target=x86_64-efi --efi-directory=/efi --bootloader-id=GRUB
grub-mkconfig -o /boot/grub/grub.cfg
exit
umount -R /mnt/arch-chroot
umount -R /mnt/subvolumes
cryptsetup close boot
cryptsetup close system
sync
reboot
```


```
sudo cfdisk /dev/nvme0n1
sudo cryptsetup benchmark
sudo cryptsetup -v luksFormat /dev/nvme0n1p5
sudo cryptsetup -v luksDump /dev/nvme0n1p5

sudo xxd /dev/nvme0n1p2
sudo xxd /dev/nvme0n1p2 | less
sudo cryptsetup open /dev/nvme0n1p2 archlinux
sudo xxd /dev/mapper/archlinux | less

sudo mkfs.ext4 /dev/mapper/archlinux
sudo mount /dev/mapper/archlinux /mnt

# remove filesystem crypto_LUKS
cryptsetup-reencrypt --decrypt /dev/nvme0n1p5
```
