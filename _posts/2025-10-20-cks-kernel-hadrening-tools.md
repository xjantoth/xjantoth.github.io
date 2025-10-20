---
title: "CKS Kernel Hardening Tools"
date: 2022-06-10T20:19:12+02:00
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS Kernel Hardening Tools"

tags: ['cks', 'kernel', 'hardening', 'tools']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##### Requirements for Apparmor

* container runtime needs to support Apparmor
* Apparmor needs to be installed on every node
* Apparmor profiles need to be available on every node
* Apparmor profiles are specified per container (done via annotations) not per pod!

![Image](/assets/images/blog/kh-1.png)
![Image](/assets/images/blog/kh-2.png)

##### AppArmor Profile Modes

![Image](/assets/images/blog/kh-3.png)
![Image](/assets/images/blog/kh-4.png)

###### Create a simple Apparmor profile for curl

```
# Install neceassary packages
apt-get install apparmor
apt-get install apparmor-utils # important!
aa-status

# Generate a profile for CURL
aa-genprof curl
```

Edit a profile according your needs

```
cat  /etc/apparmor.d/usr.bin.curl
# Last Modified: Tue Apr 13 20:23:56 2021
#include <tunables/global>

/usr/bin/curl {
  #include <abstractions/base>

  /lib/x86_64-linux-gnu/ld-*.so mr,
  /usr/bin/curl mr,

}
```

###### Load newly defined profile to Apparmor

It is very unlikely to write your own apparmor profile during an exam but one has to know:
* how to load a new apparmor profile
* how to use it in Kubernetes pod

```
# load newly defined profile
apparmor_parser /etc/apparmor.d/docker-nginx

# remove already existing profile
apparmor_parser -R /etc/apparmor.d/some-profile
```





###### Hwo to use apparmor with Docker

```
# default AppArmor profile
 docker run --security-opt apparmor=docker-default nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
f7ec5a41d630: Pull complete
aa1efa14b3bf: Pull complete
b78b95af9b17: Pull complete
c7d6bca2b8dc: Pull complete
cf16cd8e71e0: Pull complete
0241c68333ef: Pull complete
Digest: sha256:75a55d33ecc73c2a242450a9f1cc858499d468f077ea942867e662c247b5e412
Status: Downloaded newer image for nginx:latest
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up


# custom AppArmor profile
 docker run --security-opt apparmor=docker-nginx nginx
/docker-entrypoint.sh: No files found in /docker-entrypoint.d/, skipping configuration
/docker-entrypoint.sh: 13: /docker-entrypoint.sh: cannot create /dev/null: Permission denied
```

###### Create a pod which uses an Apparmor profile

![Image](/assets/images/blog/kh-5.png)


```
root@scw-k8s-cmdx:~# cat secure.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secure
  name: secure
  annotations:
    container.apparmor.security.beta.kubernetes.io/secure: localhost/docker-nginx
spec:
  containers:
  - image: nginx
    name: secure
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```


##### Seccomp (Secure Computing Mode)

![Image](/assets/images/blog/kh-6.png)

* security facility in the Linux Kernel
* restricts execution of syscalls

![Image](/assets/images/blog/kh-7.png)
![Image](/assets/images/blog/kh-8.png)
![Image](/assets/images/blog/kh-9.png)


###### Download seccomp profile:


```
wget https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/system-hardening/kernel-hardening-tools/seccomp/profile-docker-nginx.json
```

###### Use this profile with docker


```
root@scw-k8s-cmdx:~# docker run --name=hmm-with-seccomp --security-opt seccomp=profile-docker-nginx.json nginx
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
...
```

###### How about if you simply remove `write` premissions from file: `profile-docker-nginx.json`

![Image](/assets/images/blog/kh-10.png)

###### Container will not start because of missing `write` syscall
```
root@scw-k8s-cmdx:~# docker run --name=removed-write-seccomp --security-opt seccomp=profile-docker-nginx.json nginx
docker: Error response from daemon: OCI runtime start failed: cannot start an already running container: unknown.
ERRO[0001] error waiting for container: context canceled

```

##### How to create Seccomp profile in Kubernetes for kubelet


```
root@scw-k8s-cmdx:~# mkdir  /var/lib/kubelet/seccomp
root@scw-k8s-cmdx:~# cp profile-docker-nginx.json /var/lib/kubelet/seccomp/

```

###### Generate a pod according a documentation


```
root@scw-k8s-cmdx:~# cat seccomp.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: nginx
  name: nginx
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/profile-docker-nginx.json
  containers:
  - image: nginx
    name: nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```

###### Now if you run it - you will see it fails


```
root@scw-k8s-cmdx:~# k describe pod nginx
Name:         nginx
Namespace:    default
Priority:     0
...
  Warning  Failed     11s (x2 over 14s)  kubelet            Error: failed to create containerd container: cannot load seccomp profile "/var/lib/kubelet/seccomp/profiles/profile-docker-nginx.json": open /var/lib/kubelet/seccomp/profiles/profile-docker-nginx.json: no such file or directory
r
```


###### We need to create a subfolder under seccomp folder in kubelet location


```
root@scw-k8s-cmdx:~# mkdir /var/lib/kubelet/seccomp/profiles
root@scw-k8s-cmdx:~# mv /var/lib/kubelet/seccomp/profile-docker-nginx.json /var/lib/kubelet/seccomp/profiles/

root@scw-k8s-cmdx:~# k delete -f seccomp.yaml
root@scw-k8s-cmdx:~# k create -f seccomp.yaml

root@scw-k8s-cmdx:~# k get pods
NAME     READY   STATUS    RESTARTS   AGE
nginx    1/1     Running   0          6s
secure   1/1     Running   0          35m

```
