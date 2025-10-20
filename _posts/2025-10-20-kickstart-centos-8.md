---
title: "kickstart Centos 8"
date: "2022-01-07T11:16:43+0100"
lastmod: "2022-01-07T11:16:43+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/linux-1.jpg"
description: "kickstart Centos 8"

tags: ['kickstart', 'centos']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**Centos 8 ISO location''

```

wget http://merlin.fit.vutbr.cz/mirrors/centos/8.2.2004/isos/x86_64/CentOS-8.2.2004-x86_64-dvd1.iso
```

**Run this command''

```

export KS="k8s-1-210"
export ISO="CentOS-8.2.2004-x86_64-dvd1.iso"

sudo virt-install --name $KS \
--description "Centos 8 $KS" \
--ram 896 \
--vcpus 2 \
--disk path=/opt/VMs/$KS.qcow2,size=15 \
--os-type linux \
--os-variant centos8 \
--network bridge=virbr0 \
--location ~/Downloads/${ISO} \
--noautoconsole \
--initrd-inject ks_$KS.cfg \
--extra-args=ks="file:/ks_$KS.cfg net.ifnames=0"

```

**Example'' file: ''ks_k8s-1-210.cfg''

```
# Install OS instead of upgrade
install
# Use network installation
cdrom
# Root password
rootpw toor
# System authorization information
auth --useshadow --passalgo=sha512

# Firewall configuration
firewall --disabled
# SELinux configuration
selinux --disable

# Installation logging level
logging --level=info
# Use text mode install
text
# Do not configure the X Window System
skipx
# System timezone, language and keyboard
timezone --utc Europe/Copenhagen
lang en_US.UTF-8
#keyboard dk-latin1
# Network information
# network  --bootproto=static --ip=192.168.122.110 --device=eth0 --onboot=on
# If you want to configure a static IP:
network --device eth0 --hostname k8s-1-210 --bootproto=static --ip=192.168.122.210 --netmask=255.255.255.0 --gateway=192.168.122.1 --nameserver 192.168.122.1

# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Disk partitioning information
#part /boot --fstype="ext4" --size=512
#part swap --fstype="swap" --recommended
part swap --fstype="swap" --size=1408
#part /var --fstype="ext4" --size=5120 --grow
part / --fstype="ext4" --size=1024 --grow
#part /usr --fstype="ext4" --size=3072
#part /home --fstype="ext4" --size=512
#part /tmp --fstype="ext4" --size=1024

# Reboot after installation
reboot

%packages
@core
# vim
#authselect-compat
yum-utils
iscsi-initiator-utils
pkgconf-pkg-config
%end

%post --log=/root/ks-post.log

echo "net.bridge.bridge-nf-call-ip6tables=1
net.bridge.bridge-nf-call-iptables=1" > /etc/sysctl.conf

#---- Install our SSH key ----
mkdir -m0700 /root/.ssh/
cat <<EOF >/root/.ssh/authorized_keys
ssh-rsa AAAA...1 rancher@k8s
EOF
chmod 0600 /root/.ssh/authorized_keys
restorecon -R /root/.ssh/authorized_keys

# install iptables-legacy
#rpm -Uvh http://192.168.1.12:8000/iptables-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-arptables-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-debuginfo-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-debugsource-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-devel-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-ebtables-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-legacy-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-legacy-debuginfo-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-libs-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-libs-debuginfo-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-services-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-utils-1.8.4-20.el8.x86_64.rpm http://192.168.1.12:8000/iptables-utils-debuginfo-1.8.4-20.el8.x86_64.rpm
#
#alternatives --install /usr/sbin/iptables iptables /usr/sbin/xtables-legacy-multi 1
#
# Install kubernetes
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install k8s goodies
dnf install -y --nobest docker-ce kubeadm

systemctl enable docker
systemctl enable kubelet
systemctl enable iscsid

%end

```
