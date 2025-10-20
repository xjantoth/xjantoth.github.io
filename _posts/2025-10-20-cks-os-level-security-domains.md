---
title: "CKS OS Level Security Domains"
date: 2022-05-24T19:22:09+0200
lastmod: 2022-05-24T19:22:09+0200
draft: false
description: "CKS OS Level Security Domains"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'os', 'level', 'security', 'domains']
---

###### Define privilege and access control for Pod/Container

* userID and GroupID
* run privileged or *unprivileged*
* Linux Capabilities


![Image](/assets/images/blog/sc-1.png)
![Image](/assets/images/blog/sc-2.png)


###### Run a simple container and check user and group

```
root@scw-k8s:~# k run pod --image=busybox --command -oyaml --dry-run=client -- sh -c 'sleep 1d' > bb.yaml
root@scw-k8s:~# k create -f  bb.yaml
```

###### Now let's try to setup a security context at a pod level

Edit container recipt first


```
root@scw-k8s:~# cat bb.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
  securityContext:
    runAsUser: 1000    # <<< notice
    runAsGroup: 3000   # <<< notice
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```

###### Once pod is created you do not have permissions to create a file in `/root` directory :)

```
root@scw-k8s:~# k exec -it pod -- sh
/ $ id
uid=1000 gid=3000
/ $ touch test
touch: test: Permission denied
/ $ touch /tmp/sss.txt
/ $ ls -l /tmp/sss.txt
-rw-r--r--    1 1000     3000             0 May 30 18:50 /tmp/sss.txt
/ $

```


###### Run pod with a flag `runAsNonRoot: true`

Hmm and YOU will see that it actually runs! Why???
Because we have specified a `securityContext` at the pod level with values 1000 for user and 3000 for a group previously!

```
root@scw-k8s:~# cat bb.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: pod
    resources: {}
    securityContext:
      runAsNonRoot: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```


###### Let's try to comment out the first `securityContext` section level and see what happens


```
root@scw-k8s:~# cat  bb.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
#  securityContext:
#    runAsUser: 1000
#    runAsGroup: 3000
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: pod
    resources: {}
    securityContext:
      runAsNonRoot: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

And check the actuall error


```
root@scw-k8s:~# k get pods
NAME     READY   STATUS                       RESTARTS   AGE
gvisor   0/1     ContainerStatusUnknown       1          12d
pod      0/1     CreateContainerConfigError   0          5s

root@scw-k8s:~# k describe  pod pod
Name:         pod
Namespace:    default
Priority:     0
Node:         scw-k8s/10.18.164.57
...
...

  Warning  Failed     4s (x4 over 37s)  kubelet            Error: container has runAsNonRoot and image will run as root (pod: "pod_default(3f4f06af-ff78-48eb-89cb-08c3c511d9c1)", container: pod)
  Normal   Pulled     4s                kubelet            Successfully pulled image "busybox" in 1.004495509s
r
```


###### Privileged Container

* by default Docker containers run **unprivileged**
* it is possible to run privileged
  - access all devices
  - run docker daemon inside container (`docker run --privileged`)
* what it means when running privileged??
  - well container user 0 (root) maps **directly** to host user 0 (root)


```
root@scw-k8s:~# cat bb.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
#  securityContext:
#    runAsUser: 1000
#    runAsGroup: 3000
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: pod
    resources: {}
    securityContext:
      # runAsNonRoot: true
      privileged: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

Now, we were able to run `sysctl` command inside a container (very dangerous!!!)


```

/ # sysctl kernel.hostname=attacker
kernel.hostname = attacker
```


###### PrivilegeEscalation `allowPrivilegeEscalation`

* by default - it is enabled in Kubernetes

![Image](/assets/images/blog/sc-3.png)


```
root@scw-k8s:~# cat  bb.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
#  securityContext:
#    runAsUser: 1000
#    runAsGroup: 3000
  containers:
  - command:
    - sh
    - -c
    - sleep 1d
    image: busybox
    name: pod
    resources: {}
    securityContext:
      # runAsNonRoot: true
      # privileged: true
      allowPrivilegeEscalation: false
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```

Let's check it out

```
root@scw-k8s:~# k exec -it pod -- sh
/ # cat /proc/1/status
Name:   sleep
Umask:  0022
State:  S (sleeping)
Tgid:   1
...
...
...
NoNewPrivs:     1   # <<<    notice this setting
Seccomp:        0
voluntary_ctxt_switches:        28
nonvoluntary_ctxt_switches:     288

```

###### Pod Security Policies

* cluster level resource
* created by Kubenretes cluster administrator
* it is an **admission controller** and has to be allowed!!!

![Image](/assets/images/blog/sc-4.png)
![Image](/assets/images/blog/sc-5.png)
![Image](/assets/images/blog/sc-6.png)
![Image](/assets/images/blog/sc-7.png)

Setup `kube-apiserver` first, since **PodSecurityPolicy** is an adminssion controller


```
root@scw-k8s:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml  | grep admiss -B10 -A3
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.18.164.57
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction,PodSecurityPolicy  # <<< --- add this text behind comma!
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
```

Create your very first pod security policy


```
root@scw-k8s:~# cat psp.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: cks-psp
spec:
  privileged: false  # Don't allow privileged pods!
  # The rest fills in some required fields.
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  volumes:
  - '*'
```

Now, you will not be able to create pretty much anything since `default serviceaccount` does not have any permissions to use `podsecuritypolicies k8s objects` at all.


```
k create role psp --verb=use --resource=podsecuritypolicies
k create rolebinding psp-rb --role psp --serviceaccount=default:default
```

How, about creating a deployment?


```
# It is gonna work now :)
root@scw-k8s:~# k create  deployment jano --image=nginx:alpine
root@scw-k8s:~# k get deploy
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
jano   1/1     1            1           11m
```


The following deployment is going to fail since we want to use `privileged: true` option. This option is specifically disabled by `podsecuritypolicies` we created a while ago.

```
root@scw-k8s:~# k create deployment cks-psp \
--image=nginx:alpine --replicas=3 \
-oyaml --dry-run=client \
| sed -E 's/^(\s+- image.*)$/\1 \n        securityContext:\n          privileged: true/'  | k create -f -
deployment.apps/cks-psp created

root@scw-k8s:~# k get events | grep cks-psp
5s          Warning   FailedCreate        replicaset/cks-psp-79fc878f85   Error creating: pods "cks-psp-79fc878f85-" is forbidden: PodSecurityPolicy: unable to admit pod: [spec.containers[0].securityContext.privileged: Invalid value: true: Privileged containers are not allowed]
46s         Normal    ScalingReplicaSet   deployment/cks-psp              Scaled up replica set cks-psp-79fc878f85 to 3

```

Let's do a bit more exercise and try to comply with our `podsecuritypolicies`.


```
root@scw-k8s:~# k create deployment cks-psp-will-work --image=nginx:alpine --replicas=3 -oyaml --dry-run=client | sed -E 's/^(\s+- image.*)$/\1 \n        securityContext:\n          privileged: false/'  | k create -f -
deployment.apps/cks-psp-will-work created

root@scw-k8s:~# k get deploy
NAME                READY   UP-TO-DATE   AVAILABLE   AGE
cks-psp             0/3     0            0           2m46s
cks-psp-will-work   3/3     3            3           43s
```

###### Create a privileged pod


```
# is CKS simulator
k run prime --image=nginx:alpine --privileged=true --command -o yaml --dry-run=client -- sh -c 'apk add iptables && sleep 1d' | k create -f -
pod/prime created
```

###### Disable allowPrivilegeEscalation


```
controlplane $ k get deployments.apps logger -oyaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
  creationTimestamp: "2022-06-03T09:26:23Z"
  generation: 2
  labels:
    app: logger
  name: logger
  namespace: default
  resourceVersion: "1580"
  uid: d46deaf9-c544-4062-8d84-becbfa2ad4ba
spec:
  progressDeadlineSeconds: 600
  replicas: 3
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: logger
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: logger
    spec:
      containers:
      - command:
        - sh
        - -c
        - while true; do cat /proc/1/status | grep NoNewPrivs; sleep 1; done
        image: bash:5.0.18-alpine3.14
        imagePullPolicy: IfNotPresent
        name: httpd
        resources: {}
        securityContext:
          allowPrivilegeEscalation: false
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 0
status:
  availableReplicas: 3
  ...
  replicas: 3
  updatedReplicas: 3
```
