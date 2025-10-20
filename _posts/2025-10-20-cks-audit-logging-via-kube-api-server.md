---
title: "CKS Audit logging via kube-api server"
date: 2022-06-09T21:48:40+02:00
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS Audit logging via kube-api server"

tags: ['cks', 'audit', 'logging', 'via', 'server']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


![Image](/assets/images/blog/al-0.png)

![Image](/assets/images/blog/al-1.png)
![Image](/assets/images/blog/al-2.png)

##### Important Kubernetes request stages

![Image](/assets/images/blog/al-3.png)
![Image](/assets/images/blog/al-4.png)

##### What events should be recorded

![Image](/assets/images/blog/al-5.png)
![Image](/assets/images/blog/al-6.png)

Audit log from Mushad course

##### An example of Audit Policy object

```yaml
apiVersion: audit.k8s.io/v1 # This is required.
kind: Policy
# Don't generate audit events for all requests in RequestReceived stage.
omitStages:
  - "RequestReceived"
rules:
  # Log pod changes at RequestResponse level
  - level: Metadata
    namespace: ["prod"]
    verb: ["delete"]
    resources:
    - group: ""
      # Resource "pods" doesn't match requests to any subresource of pods,
      # which is consistent with the RBAC policy.
      resources: ["secrets"]
  # Log "pods/log", "pods/status" at Metadata level
```


##### Kube-apiserver configuration

Now, we need to create an extra folder for auditing

```
mkdir -p /var/log/kubernetes/audit
```

Create Policy file within this folder

```yaml
apiVersion: audit.k8s.io/v1 # This is required.
kind: Policy
rules:
  - level: Metadata
```



Policy file: `/etc/kubernetes/audit/policy.yaml`

```yaml
cat /etc/kubernetes/audit/policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
```

Advanced Policy file: /etc/kubernetes/audit/policy.yaml

```yaml
 cat  /etc/kubernetes/audit/policy.yaml
apiVersion: audit.k8s.io/v1 # This is required.
kind: Policy

# Don't generate audit events for all requests in RequestReceived stage.
# 1. Nothing from stage RequestReceived
omitStages:
  - "RequestReceived"

rules:
  - level: None
    # 2. Nothing from "watch", "list", "get"
    verbs: ["watch", "list", "get"]

  - level: Metadata
    resources:
    # 3. From Secrets only metadata level
    - group: "" # core API group
      resources: ["secrets"]
    # 4. log evrything related to "RequestResponse"
  - level: RequestResponse



```

Kube-api server file: `/etc/kubernetes/manifests/kube-apiserver.yaml`

https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/#log-backend

Log backend
The log backend writes audit events to a file in JSONlines format. You can configure the log audit backend using the following kube-apiserver flags:

```
--audit-log-path specifies the log file path that log backend uses to write audit events. Not specifying this flag disables log backend. - means standard out
--audit-log-maxage defined the maximum number of days to retain old audit log files
--audit-log-maxbackup defines the maximum number of audit log files to retain
--audit-log-maxsize defines the maximum size in megabytes of the audit log file before it gets rotated
```

If your cluster's control plane runs the kube-apiserver as a Pod, remember to mount the hostPath to the location of the policy file and log file, so that audit records are persisted. For example:

```
    --audit-policy-file=/etc/kubernetes/audit-policy.yaml \
    --audit-log-path=/var/log/kubernetes/audit/audit.log
```

then mount the volumes:

```
...
volumeMounts:
  - mountPath: /etc/kubernetes/audit-policy.yaml
    name: audit
    readOnly: true
  - mountPath: /var/log/kubernetes/audit/
    name: audit-log
    readOnly: false
```

and finally configure the hostPath:


```yaml
...
volumes:
- name: audit
  hostPath:
    path: /etc/kubernetes/audit-policy.yaml
    type: File

- name: audit-log
  hostPath:
    path: /var/log/kubernetes/audit/
    type: DirectoryOrCreate
```

![Image](/assets/images/blog/al-7.png)

Solution:

```
root@scw-k8s-cmdx:~# cat  /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  - level: RequestResponse
  - level: None
    verbs: ["watch","get","list"]
  - level: Metadata
    resources:
    - group: "" # core API group
      resources: ["secrets"]

```

![Image](/assets/images/blog/al-8.png)


```
root@scw-k8s-cmdx:~# cat /etc/kubernetes/audit-policy.yaml
apiVersion: audit.k8s.io/v1
kind: Policy
omitStages:
  - "RequestReceived"
rules:
  # log nothing regarding events
  - level: None
    resources:
    - group: "" # core
      resources: ["events"]

  # log nothing coming from some components
  - level: None
    users:
    - "system:kube-scheduler"
    - "system:kube-proxy"
    - "system:apiserver"
    - "system:kube-controller-manager"
    - "system:serviceaccount:gatekeeper-system:gatekeeper-admin"

  # log nothing coming from some groups
  - level: None
    userGroups: ["system:nodes"]

  - level: None
    verbs: ["watch","get","list"]
  - level: RequestResponse
    resources:
    - group: "" # core API group
      resources: ["secrets"]

  - level: RequestResponse
```
