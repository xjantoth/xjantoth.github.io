---
title: "cks-benchmakring.md"
date: 2022-02-22T10:15:12+0100
lastmod: 2022-02-22T10:15:12+0100
draft: false
description: "cks-benchmakring.md"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'benchmarking']
---

## CSI Kubernetes Benchmark 1.6.0 (at the time)

Make sure to check CSI vs. current Kubernetes version
You have got some recommendations to improve Kubenretes cluster security

## Aquasecurity Kubebench


```bash
# When using lima and nerdctl
limactl shell k8s \
sudo nerdctl -n k8s.io --address /run/containerd/containerd.sock \
run --pid=host \
-v /etc:/etc:ro \
-v /var:/var:ro \
-it aquasec/kube-bench:latest \
run --targets=master --version 1.23


# how to run
https://github.com/aquasecurity/kube-bench/blob/main/docs/running.md
# run on master
docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t aquasec/kube-bench:latest run --targets=master --version 1.22
# run on worker
docker run --pid=host -v /etc:/etc:ro -v /var:/var:ro -t aquasec/kube-bench:latest run --targets=node --version 1.22
```


###### Kube-bench in action (fix FAILED checks)


```bash
controlplane $ kube-bench run --targets master --check 1.3.2
[INFO] 1 Master Node Security Configuration
[INFO] 1.3 Controller Manager
[FAIL] 1.3.2 Ensure that the --profiling argument is set to false (Automated)

== Remediations master ==
1.3.2 Edit the Controller Manager pod specification file /etc/kubernetes/manifests/kube-controller-manager.yaml
on the master node and set the below parameter.
--profiling=false


== Summary master ==
0 checks PASS
1 checks FAIL
0 checks WARN
0 checks INFO

== Summary total ==
0 checks PASS
1 checks FAIL
0 checks WARN
0 checks INFO

# Now check

Fix the /etc/kubernetes/manifests/kube-controller-manager.yaml


...
  containers:
  - command:
    - kube-controller-manager
    - --profiling=false
...
    image: k8s.gcr.io/kube-controller-manager:v1.22.2
...
```
