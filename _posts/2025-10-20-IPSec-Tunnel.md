---
title: "IPSec Tunnel"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "IPSec Tunnel"

tags: ['ml', 'ipsec', 'tunnel']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```py
# LAPTOP
cat /etc/ipsec.conf
config setup

conn laptop
     authby=secret
     pfs=yes
     auto=start
     keyingtries=3
     dpddelay=30
     dpdtimeout=120
     dpdaction=clear
     ikelifetime=8h
     ikev2=no
     keylife=1h
     #phase2alg=aes128-sha1;modp1024
     #ike=aes128-sha1;modp1024
     type=tunnel
     left=%defaultroute
     leftsubnet=192.168.1.0/24
     leftid=88.212.33.167  # u mna doma verejna na routeri
     rightsubnet=172.31.0.0/20
     right=18.237.195.235   # EC2 v AWS
```


```py
# AWS EC2
cat /etc/ipsec.conf.bavi
config setup

conn aws-ec2
     authby=secret
     pfs=yes
     auto=start
     keyingtries=3
     dpddelay=30
     dpdtimeout=120
     dpdaction=clear
     ikelifetime=8h
     keylife=1h
     #phase2alg=aes128-sha1;modp1024
     #ike=aes128-sha1;modp1024
     type=tunnel
     ikev2=no
     right=88.212.33.167  # u mna doma verejna na routeri
     rightsubnet=192.168.1.0/24
     left=%defaultroute   # EC2 v AWS
     leftid=18.237.195.235   # EC2 v AWS
     leftsubnet=172.31.0.0/20
```


```py
cat /etc/ipsec.secrets
88.212.33.167 18.237.195.235 : PSK "..."
```


##  set route via ipsec tunnel node


* run on other hosts in network


```py
sudo ip r add  172.31.0.0/20 via 192.168.1.144 dev wlan0
ip r get 172.31.12.119
```


##  disable redirect to allow all hosts in network to access other network hosts


* run on ipsec node


```py
echo 0 | sudo tee /proc/sys/net/ipv4/conf/*/send_redirects


sudo ip r flush cache
openssl rand -hex 32

# Check this setting t your PC (laptop)
sysctl net.ipv4.ip_forward=1


cat  /etc/sysctl.d/97-vpn.conf
net.ipv4.ip_forward = 1
net.ipv4.conf.all.send_redirects = 0


# 91.127.47.154 88.212.33.167 : PSK "a...22959da18"
%any : PSK "a...22959da18"


conn vpn
     authby=secret
     auto=start
     type=tunnel
     ikev2=insist

     left=%defaultroute
     leftsubnet=192.168.2.0/24
     leftid=88.212.33.167

     rightsubnet=192.168.1.0/24
     right=91.127.47.154

```
