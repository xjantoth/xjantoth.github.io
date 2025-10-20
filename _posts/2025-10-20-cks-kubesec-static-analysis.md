---
title: "CKS Kubesec - Security risk analysis for Kubernetes resources"
date: 2022-06-05T18:22:00+02:00
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS Kubesec - Security risk analysis for Kubernetes resources"

tags: ['cks', 'kubesec', 'security', 'risk', 'analysis', 'kubernetes', 'resources']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##### Static Analysis
- manual approach
- kubesec
- OPA Conftest


###### Notes

* can be incorporated in CI/CD system
* looks at source code and text files
* check against rules
* enforce rules e.g:
  - "Always define resource requests and limits"
  - "Pod should never use the default ServiceAccount"

![Image](/assets/images/blog/sa-1.png)

###### Kubesec

- security risk analysis for Kubernetes resources
- opensource
- opinionated (fixed set of rules - security best practices)
- runs as (binary, docker container, kubectl plugin, admission controller)

```
wget https://github.com/controlplaneio/kubesec/releases/download/v2.11.0/kubesec_linux_amd64.tar.gz
tar -xvzf kubesec_linux_amd64.tar.gz
mv kubesec /usr/bin/kubesec
kubesec
```

###### Scan your resources

```
Examples:
  kubesec scan ./deployment.yaml
  cat file.json | kubesec scan -
  helm template -f values.yaml ./chart | kubesec scan /dev/stdin
```

###### Simple usecase

```
kubectl  run pod --image=nginx -oyaml --dry-run=client > file
cat file | kubesec  scan -o yaml -

[
  {
    "object": "Pod/pod.default",
    "valid": true,
    "fileName": "STDIN",
    "message": "Passed with a score of 0 points",
    "score": 0,
    "scoring": {
      "advise": [
        {
          "id": "ApparmorAny",
          "selector": ".metadata .annotations .\"container.apparmor.security.beta.kubernetes.io/nginx\"",
          "reason": "Well defined AppArmor policies may provide greater protection from unknown threats. WARNING: NOT PRODUCTION READY",
          "points": 3
        },
        {
          "id": "ServiceAccountName",
          "selector": ".spec .serviceAccountName",
          "reason": "Service accounts restrict Kubernetes API access and should be configured with least privilege",
          "points": 3
        },
...

```

###### Another example
cat node.yaml | kubesec  scan -o yaml - > /root/kubesec_report.json


```
root@scw-k8s:~# k run nginx --image=nginx:alpine -oyaml --dry-run=client > pod.yaml
root@scw-k8s:~# curl -sSX POST --data-binary @"pod.yaml" https://v2.kubesec.io/scan

```


###### Conftest Kubernetes - OPA

* unit test framework for Kubernetes configuration
* uses the same Rego language

![Image](/assets/images/blog/sa-2.png)



```
root@scw-k8s:~# git clone https://github.com/killer-sh/cks-course-environment.gitvb
root@scw-k8s:~/cks-course-environment# cd course-content/supply-chain-security/static-analysis/conftest/

ls -al
total 16
drwxr-xr-x 4 root root 4096 Jun  5 18:54 .
drwxr-xr-x 3 root root 4096 Jun  5 18:54 ..
drwxr-xr-x 3 root root 4096 Jun  5 18:54 docker
drwxr-xr-x 3 root root 4096 Jun  5 18:54 kubernetes

cd kubernetes
```

`Kubenetes deployment` we would like to check

```
# deployment we would like to check
cat deploy.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: test
  name: test
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: test
    spec:
      containers:
        - image: httpd
          name: httpd
          resources: {}
status: {}
```


Policy file for our `Kubernetes deployment` (set of rules to follow)

```
cat policy/deployment.rego
# from https://www.conftest.dev
package main

deny[msg] {
  input.kind = "Deployment"
  not input.spec.template.spec.securityContext.runAsNonRoot = true
  msg = "Containers must not run as root"
}

deny[msg] {
  input.kind = "Deployment"
  not input.spec.selector.matchLabels.app
  msg = "Containers must provide app label for pod selectors"
}
```

Run conftest to check `Kubernetes deployment`

```
docker run --rm -v $(pwd):/project openpolicyagent/conftest test deploy.yaml
FAIL - deploy.yaml - main - Containers must not run as root

2 tests, 1 passed, 0 warnings, 1 failure, 0 exceptions
```

###### Use conftest OPA for Dockerfile

```
root@scw-k8s:~# git clone https://github.com/killer-sh/cks-course-environment.git
root@scw-k8s:~/cks-course-environment# cd course-content/supply-chain-security/static-analysis/conftest/

cd docker

```

Example of policy files


```
# from https://www.conftest.dev           |# from https://www.conftest.dev
package main                              |
                                          |package commands
denylist = [                              |
  "ubuntu"                                |denylist = [
]                                         |  "apk",
                                          |  "apt",
deny[msg] {                               |  "pip",
  input[i].Cmd == "from"                  |  "curl",
  val := input[i].Value                   |  "wget",
  contains(val[i], denylist[_])           |]
                                          |
  msg = sprintf("unallowed image found %s"|deny[msg] {
, [val])                                  |  input[i].Cmd == "run"
}                                         |  val := input[i].Value
                                          |  contains(val[_], denylist[_])
                                          |
                                          |  msg = sprintf("unallowed commands found
                                          | %s", [val])
                                          |}
                                          |~

```

`Dockerfile` to be checked


```
cat Dockerfile
FROM ubuntu
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y golang-go
COPY app.go .
RUN go build app.go
CMD ["./app"]
```

Run command to chceck `Dockerfile` via OPA conftest tool


```
docker run --rm -v $(pwd):/project openpolicyagent/conftest test Dockerfile --all-namespaces
FAIL - Dockerfile - main - unallowed image found ["ubuntu"]
FAIL - Dockerfile - commands - unallowed commands found ["apt-get update && apt-get install -y golang-go"]

2 tests, 0 passed, 0 warnings, 2 failures, 0 exceptions
```
