---
title: "CKS Trivy and Clair - Vulnerability Scanner for Containers and other Artifacts"
date: 2022-06-05T21:30:20+02:00
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS Trivy and Clair - Vulnerability Scanner for Containers and other Artifacts"

tags: ['cks', 'trivy', 'clair', 'vulnerability', 'scanner', 'containers', 'other', 'artifacts']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

![Image](/assets/images/blog/iv-1.png)
![Image](/assets/images/blog/iv-2.png)
![Image](/assets/images/blog/iv-3.png)

##### There are Clair and Trivy

1. `trivy` (run one command - very convinient)
    - open source
    - easy to run

2. `clair`
    - open source
    - static analysis of vulnerabilities in application containers
    - ingest vulnerability metadata froma configured set of sources
    - provides API

###### How to install trivy

```
wget https://github.com/aquasecurity/trivy/releases/download/v0.17.2/trivy_0.17.2_Linux-64bit.tar.gz
tar -xvzf trivy_0.17.2_Linux-64bit.tar.gz
mv trivy /usr/bin/
trivy
```

Example of usage

```
trivy image --severity HIGH python:3.6.12-alpine3.11 > /root/python.txt
```

Scan tarball

```
trivy image --format  json -i alpine.tar > /root/alpine.json
root@controlplane:~# cat /root/alpine.json
root@controlplane:~# cat !$
cat /root/alpine.json
2021-05-06T08:20:06.586Z        INFO    Detecting Alpine vulnerabilities...
2021-05-06T08:20:06.587Z        INFO    Trivy skips scanning programming language libraries because no supported file was detected
[
  {
    "Target": "alpine.tar (alpine 3.13.5)",
    "Type": "alpine",
    "Vulnerabilities": null
  }
```

###### How to run trivy as docker image

source: https://github.com/aquasecurity/trivy#docker

```
docker run ghcr.io/aquasecurity/trivy:latest image nginx:latest
Unable to find image 'ghcr.io/aquasecurity/trivy:latest' locally
latest: Pulling from aquasecurity/trivy
df9b9388f04a: Pull complete
d357a848ae49: Pull complete
feaac6a5c940: Pull complete
6132b2ff13cc: Pull complete
Digest: sha256:c97cc414cfddd63d4933c0bb511493a9636e535b0d6db0fa0153fcf232ce8bf2
Status: Downloaded newer image for ghcr.io/aquasecurity/trivy:latest
2022-06-05T19:45:32.012Z        INFO    Need to update DB
...
2022-06-05T19:46:08.396Z        INFO    Detecting Debian vulnerabilities...
2022-06-05T19:46:08.564Z        INFO    Number of language-specific files: 0

nginx:latest (debian 11.3)
==========================
Total: 138 (UNKNOWN: 0, LOW: 93, MEDIUM: 21, HIGH: 18, CRITICAL: 6)

┌──────────────────┬──────────────────┬──────────┬───────────────────────┬───────────────┬──────────────────────────────────────────────────────────────┐
│     Library      │  Vulnerability   │ Severity │   Installed Version   │ Fixed Version │                            Title                             │
├──────────────────┼──────────────────┼──────────┼───────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ apt              │ CVE-2011-3374    │ LOW      │ 2.2.4                 │               │ It was found that apt-key in apt, all versions, do not       │
│                  │                  │          │                       │               │ correctly...                                                 │
│                  │                  │          │                       │               │ https://avd.aquasec.com/nvd/cve-2011-3374                    │
├──────────────────┼──────────────────┼──────────┼───────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ tar              │ CVE-2005-2541    │ LOW      │ 1.34+dfsg-1           │               │ tar: does not properly warn the user when extracting setuid  │
│                  │                  │          │                       │               │ or setgid...                                                 │
│                  │                  │          │                       │               │ https://avd.aquasec.com/nvd/cve-2005-2541                    │
├──────────────────┼──────────────────┤          ├───────────────────────┼───────────────┼──────────────────────────────────────────────────────────────┤
│ util-linux       │ CVE-2022-0563    │          │ 2.36.1-8+deb11u1      │               │ util-linux: partial disclosure of arbitrary files in chfn    │
│                  │                  │          │                       │               │ and chsh when compiled...                                    │
│                  │                  │          │                       │               │ https://avd.aquasec.com/nvd/cve-2022-0563                    │
└──────────────────┴──────────────────┴──────────┴───────────────────────┴───────────────┴──────────────────────────────────────────────────────────────┘

```

##### Challenge

Scan images in Namespaces applications and infra for the vulnerabilities CVE-2021-28831 and CVE-2016-9841 .
Scale those Deployments containing any of these down to 0 .

```
trivy  image  $(k get deployments.apps -n applications web1 -ojsonpath='{.spec.template.spec.containers[*].image}') | grep -E "CVE-2021-28831|CVE-2016-9841"
trivy  image  $(k get deployments.apps -n applications web2 -ojsonpath='{.spec.template.spec.containers[*].image}') | grep -E "CVE-2021-28831|CVE-2016-9841"
trivy  image  $(k get deployments.apps -n infra inf-hjk -ojsonpath='{.spec.template.spec.containers[*].image}') | grep -E "CVE-2021-28831|CVE-2016-9841"

k scale deployment -n applications web1 --replicas=0
k scale deployment -n infra inf-hjk --replicas=0
```
