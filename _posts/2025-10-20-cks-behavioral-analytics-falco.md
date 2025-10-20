---
title: "CKS behavioral analytics falco"
date: 2022-06-07T13:29:03+02:00
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS behavioral analytics falco"

tags: ['cks', 'behavioral', 'analytics', 'falco']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


![Image](/assets/images/blog/fa-1.png)
![Image](/assets/images/blog/fa-2.png)
![Image](/assets/images/blog/fa-3.png)

###### Explore strace


```
root@scw-k8s:~# strace -cw ls /
bin   etc         initrd.img.old  lost+found  opt   run   srv  usr      vmlinuz.old
boot  home        lib             media       proc  sbin  sys  var
dev   initrd.img  lib64           mnt         root  snap  tmp  vmlinuz
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 25.62    0.001440         480         3           write
 15.62    0.000878          30        29           mmap
 11.03    0.000620         620         1           execve
 10.21    0.000574          24        24         1 openat
  8.06    0.000453         227         2           getdents
  6.19    0.000348          14        25           close
  5.57    0.000313          13        24           fstat
  4.59    0.000258          29         9           read
  4.59    0.000258          22        12           mprotect
  3.01    0.000169          21         8         8 access
  1.00    0.000056          28         2           ioctl
  0.87    0.000049          25         2         2 statfs
  0.64    0.000036          12         3           brk
  0.53    0.000030          30         1           munmap
  0.53    0.000030          30         1           prlimit64
  0.50    0.000028          14         2           rt_sigaction
  0.37    0.000021          21         1           stat
  0.23    0.000013          13         1           rt_sigprocmask
  0.23    0.000013          13         1           set_robust_list
  0.20    0.000011          11         1           arch_prctl
  0.20    0.000011          11         1           futex
  0.20    0.000011          11         1           set_tid_address
------ ----------- ----------- --------- --------- ----------------
100.00    0.005620                   154        11 total
```


###### Falco - finds malicious processes

* cloud-native runtime security (CNFC)
* access (deep kernel tracing built on the Linux kernel)
* assert (describe security rules against a susyem + default ones, detects unwanted behaviour)
* action (automated respond to a security violations)


```

# install falco
curl -s https://falco.org/repo/falcosecurity-3672BA8F.asc | apt-key add -
echo "deb https://dl.bintray.com/falcosecurity/deb stable main" | tee -a /etc/apt/sources.list.d/falcosecurity.list
apt-get update -y
apt-get -y install linux-headers-$(uname -r)
apt-get install -y falco

# docs about falco
https://v1-16.docs.kubernetes.io/docs/tasks/debug-application-cluster/falco

systemctl enable --now falco
journalctl -f -u falco
```



![Image](/assets/images/blog/fa-4.png)
