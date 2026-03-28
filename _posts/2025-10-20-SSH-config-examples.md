---
title: "SSH config examples"
date: "2022-01-06T14:48:22+0100"
lastmod: "2022-01-06T14:48:22+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&h=420&fit=crop"
description: "Practical examples for configuring SSH clients, including jump hosts, agent forwarding, and per-host identity files."

tags: ['ssh', 'config']
categories: ["Networking"]
---

The SSH config file (`~/.ssh/config`) allows you to define per-host connection settings such as identity files, jump proxies, and agent forwarding. Below are several common patterns including AWS CodeCommit access, bastion/jump host setups, and GitLab SSH key configuration.

```ssh-config

vim ~/.ssh/config
...

Host git-codecommit.*.amazonaws.com
  User A...SVRJMWFPY
  IdentityFile ~/.ssh/kops-aws

Host  1.2.3.4
  HostName  1.2.3.4
  ForwardAgent yes
  User ec2-user
  AddKeysToAgent yes
  IdentityFile ~/Downloads/cert-developer.pem


# Example with JUMP server
Host e2-bastion  11.22.33.44
  HostName 11.22.33.44
  ForwardAgent yes
  User ec2-user
  AddKeysToAgent yes
  IdentitiesOnly yes
  IdentityFile ~/.ssh/bastion.id_rsa

Host final-server 44.55.66.77
  HostName 44.55.66.77
  ForwardAgent yes
  User ec2-user
  Port 22
  AddKeysToAgent yes
  IdentitiesOnly yes
  IdentityFile ~/.ssh/bastion.id_rsa
  ProxyCommand ssh -q -W %h:%p e2-bastion


# linuxinuse account
Host gitlab.websupport.sk
        HostName gitlab.websupport.sk
        User git
        IdentitiesOnly yes
        IdentityFile ~/.ssh/websupport-ssh
...
:wq!

```
