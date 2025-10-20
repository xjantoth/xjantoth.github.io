---
title: "Ansible k3sup installation"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Ansible k3sup installation"

tags: ["ml", "ansible", "k3s", "k3sup", "wrt"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Setup DD WRT /etc/hosts


```bash

```bash
ssh root@192.168.1.1
~ vi /etc/hosts
...
192.168.1.111 ip-11-112-11-111.antik.sk
192.168.1.144 rancher.k3s
...
\:wq!
~ killall -1 dnsmasq

# Generate SSH keys
ssh-keygen -t rsa -C "k3s-ansible" -N '' -f ~/.ssh/k3s-ansible

# Provision EC2 instance in AWS via Ansible playbook
ansible-playbook -i inventory/hosts.ini ec2-playbook.yml --ask-vault-pass

# Provision VirtualBox machines at your local
# Kubernetes K3S master (192.168.1.111)
cd vms/ubuntu1
vagrant up
# Kubernetes K3S node (192.168.1.222)
cd vms/ubuntu2
vagrant up

# Setup port forwarding at DD WRT

# Adjust /etc/hosts file
vim /etc/hosts
...
192.168.1.108        k3s-rpi-1
192.168.1.111        k3s-ubuntu-1-20-04
192.168.1.222        k3s-ubuntu-2-20-04
aaa.bbb.ccc.ddd      k3s-ubuntu-3-20-04
\:wq!

# Adjust inventory/hosts.ini
cat inventory/hosts.ini
k3s-rpi-1            ansible_host=192.168.1.108
k3s-ubuntu-1-20-04   ansible_host=192.168.1.111
k3s-ubuntu-2-20-04   ansible_host=192.168.1.222
k3s-ubuntu-3-20-04   ansible_host=111.222.333.444   # AWS
...

# Adjust your ~/.zshrc file
alias u1='ssh -i ~/.ssh/k3s-ansible  ubuntu@k3s-ubuntu-1-20-04'
alias u2='ssh -i ~/.ssh/k3s-ansible  ubuntu@k3s-ubuntu-2-20-04'
alias r1='ssh -i ~/.ssh/k3s-ansible  ubuntu@k3s-rpi-1'
alias e1='ssh -i ~/.ssh/k3s-ansible  ubuntu@k3s-ubuntu-3-20-04'

# Distribute SSH public keys at VMs, Raspberry
# raspberry pi 3 (ubuntu/raspberry)
cat ~/.ssh/k3s-ansible.pub | ssh ubuntu@k3s-rpi-1 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
# ubuntu in Virtualbox
cat ~/.ssh/k3s-ansible.pub | ssh ubuntu@k3s-ubuntu-1-20-04 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
cat ~/.ssh/k3s-ansible.pub | ssh ubuntu@k3s-ubuntu-2-20-04 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
k3sup install --ip 88.212.33.167 --ssh-key ~/.ssh/k3s-ansible --k3s-version 'v1.18.8+k3s1' --user k3s --k3s-extra-args "--cluster-secret S8p3r53cr3t"
k3sup join --server-ip 88.212.33.167 --ip 192.168.1.222 --ssh-key ~/.ssh/k3s-ansible --k3s-version 'v1.18.8+k3s1' --user k3s

# Uninstall k3s-agents, k3s server
# Ubuntu Virtualbox (vagrant provisioned)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-1-20-04 /usr/local/bin/k3s-uninstall.sh        # (master)
# Ubuntu (vagrant)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-2-20-04 /usr/local/bin/k3s-agent-uninstall.sh # (node)
# Raspberry Pi3
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-rpi-1  /usr/local/bin/k3s-agent-uninstall.sh # (node)
# AWS EC2 instance (node)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-3-20-04  /usr/local/bin/k3s-agent-uninstall.sh # (node)

# Checks routes/iptables added by vagrant
# K3s master (192.169.1.111)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-1-20-04 sudo iptables-save | grep  -e "\-A INPUT" -e "\-A OUTPUT" && ip r
-A OUTPUT -s 192.168.1.0/24 -d 88.212.33.167/32 -j DNAT --to-destination 192.168.1.111
-A INPUT -s 10.235.0.0/16 -d 192.168.1.111/32 -j ACCEPT
# K3s node (192.169.1.222)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-2-20-04 sudo iptables-save | grep  -e "\-A INPUT" -e "\-A OUTPUT" && ip r
-A OUTPUT -s 192.168.1.0/24 -d 88.212.33.167/32 -j DNAT --to-destination 192.168.1.111
-A INPUT -s 10.235.0.0/16 -d 192.168.1.222/32 -j ACCEPT
# K3s node (AWS EC2)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-ubuntu-3-20-04 sudo iptables-save | grep  -e "\-A INPUT" -e "\-A OUTPUT" && ip r
# K3s node (192.168.1.108 - raspberry pi)
ssh -i ~/.ssh/k3s-ansible ubuntu@k3s-rpi-1 sudo iptables-save | grep  -e "\-A INPUT" -e "\-A OUTPUT" && ip r

# Troubleshooting K3s agents
sudo tcpdump port 6443 -i eth1 and src 54.148.135.105 -nnvvS
# at both VirtualBox machines
sudo ip r del default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
sudo ip r add default via 192.168.1.1 dev eth1 proto dhcp metric 600
sudo iptables -A INPUT -s 10.235.0.0/16 -d 192.168.1.111/32 -j ACCEPT
# at my laptop and Raspberry Pi
sudo iptables -t nat -A OUTPUT -d 88.212.33.167 -s 192.168.1.0/24 -j DNAT --to-destination 192.168.1.111
sudo iptables --table nat --list

# Check certificate
kubectl get secret -o json k3s-serving -n kube-system | jq -r '.data["tls.crt"]' | base64 --decode | openssl x509 -noout -text

# Setup prerouting (just an example)
sudo iptables --table nat --append PREROUTING --destination 88.212.33.167 --jump DNAT --to-destination 192.168.1.111
sudo iptables -t nat -v -L -n --line-number
sudo iptables -t nat -D PREROUTING 2

# Loadbalancer
sudo cat /var/lib/rancher/k3s/agent/etc/k3s-agent-load-balancer.json
{
  "ServerURL": "https://88.212.33.167:6443",
  "ServerAddresses": [
    "192.168.1.111:6443"
  ]
}

# Setup static routes
cat << 'EOF' > /etc/netplan/01-netcfg.yaml
---
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
      - 192.168.1.222/24
      routes:
        - to: 0.0.0.0/0
          via: 192.168.1.1
          metric: 100
EOF
```
