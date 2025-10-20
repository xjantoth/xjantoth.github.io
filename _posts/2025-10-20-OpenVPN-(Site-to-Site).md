---
title: "OpenVPN (Site to Site)"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "OpenVPN (Site to Site)"

tags: ['ml', 'openvpn']
categories: ["tiddlywiki", "openvpn", "vpn"]

hiddenFromSearch: false
---

##  ''Setup'' routing table at EC2

```
ubuntu@ip-172-31-49-24:/etc/openvpn/server$ ip r
default via 172.31.48.1 dev ens5 proto dhcp src 172.31.49.24 metric 100
10.8.0.2 dev tun0 proto kernel scope link src 10.8.0.1
172.31.48.0/20 dev ens5 proto kernel scope link src 172.31.49.24
172.31.48.1 dev ens5 proto dhcp scope link src 172.31.49.24 metric 100
192.168.2.0/24 dev tun0 scope link
```

##  ''EC2'' openVPN configuration

```
ubuntu@ip-172-31-49-24:/etc/openvpn/server$ cat vpn.conf
dev tun
ifconfig 10.8.0.1 10.8.0.2
secret static.key

ubuntu@ip-172-31-49-24:/etc/openvpn/server$ sudo systemctl enable --now openvpn-server@vpn.service

```

##  ''Enable'' openVPN

```
sudo systemctl enable --now openvpn-server@vpn.service
```


##  ''Prievidza'' Jetson Nano

```
ubuntu@nano-pd:~$ ip r
default via 192.168.2.1 dev eth0 proto dhcp metric 100
10.8.0.1 dev tun0 proto kernel scope link src 10.8.0.2
169.254.0.0/16 dev eth0 scope link metric 1000
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
172.31.48.0/20 dev tun0 scope link
192.168.2.0/24 dev eth0 proto kernel scope link src 192.168.2.10 metric 100


ubuntu@nano-pd:~$ cat config
remote 44.x.x.x
dev tun
ifconfig 10.8.0.2 10.8.0.1
secret /etc/openvpn/static.key


sudo systemctl enable --now openvpn-client@vpn.service
Created symlink /etc/systemd/system/multi-user.target.wants/openvpn-client@vpn.service → /lib/systemd/system/openvpn-client@.service.


```

##  ''Kosice'' Jetson Nano

```
ubuntu@nano-ke:~$ ip r
default via 192.168.2.1 dev eth0 proto dhcp metric 100
10.8.0.0/24 via 192.168.2.10 dev eth0
10.42.0.0/24 via 10.42.0.0 dev flannel.1 onlink
10.42.1.0/24 dev cni0 proto kernel scope link src 10.42.1.1
169.254.0.0/16 dev eth0 scope link metric 1000
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1 linkdown
172.31.48.0/20 via 192.168.2.10 dev eth0
192.168.2.0/24 dev eth0 proto kernel scope link src 192.168.2.43 metric 100

```
