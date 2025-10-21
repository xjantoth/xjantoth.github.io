---
title: "CKS - Mock test 1"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "CKS - Mock test 1"

tags: ['cks', 'mock']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```yaml
controlplane $ cat 1.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx
  name: frontend-site
  namespace: omni
  annotations:
    container.apparmor.security.beta.kubernetes.io/nginx: localhost/restricted-frontend
spec:
  containers:
  - image: nginx:alpine
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /usr/share/nginx/html
      name: test-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: fe-token-5xxvl
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: node01
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: frontend-default
  serviceAccountName: frontend-default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - hostPath:
      path: /data/pages
      type: Directory
    name: test-volume
  - name: fe-token-5xxvl
    secret:
      defaultMode: 420
      secretName: fe-token-5xxvl
```


```yaml
controlplane $ cat 2.yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-xyz
  namespace: orion
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: app-xyz
    ports:
    - containerPort: 3306
      protocol: TCP
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-8rm6q
      readOnly: true
    - mountPath: /mnt/connector/password
      name: a-safe-secret
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: node01
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: default-token-8rm6q
    secret:
      defaultMode: 420
      secretName: default-token-8rm6q
  - name: a-safe-secret
    secret:
      secretName: a-safe-secret
```

3. A number of pods have been created in the delta namespace. Using the trivy tool, which has been installed on the controlplane, identify all the pods that have HIGH or CRITICAL level vulnerabilities and delete the corresponding pods.


Note: Do not modify the objects in anyway other than deleting the ones that have high or critical vulnerabilities.

```


k get pods -n delta -ojsonpath='{range .items[*]}{.metadata.name}{" trivy image --severity=HIGH,CRITICAL "}{.spec.containers[*].image}{" | grep Total\n"}{end}' > 3.yaml


k get pods -n delta -ojsonpath='{range .items[*]}{" trivy image --severity=HIGH,CRITICAL "}{.spec.containers[*].image}{" | grep Total\n"}{end}' >> 3.yaml
```


```yaml
ssh node01
cp CKS/audit.json /var/lib/kubelet/seccomp/profiles/

# executed at controlplane
controlplane $ cat 4.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: audit-nginx
  name: audit-nginx
spec:
  nodeName: node01
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/audit.json
  containers:
  - image: nginx
    name: audit-nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

# check syscalls at node01
ssh node01
cat /var/log/syslog | grep audit --color
```

```
vim +/"File below a known binary directory opened for writing" /etc/falco/falco_rules.yaml

cat  /etc/falco/falco_rules.local.yaml

# Or override/append to any rule, macro, or list from the Default Rules
- rule: Write below binary dir
  desc: an attempt to write to any file below a set of binary directories
  condition: >
    bin_dir and evt.dir = < and open_write
    and not package_mgmt_procs
    and not exe_running_docker_save
    and not python_running_get_pip
    and not python_running_ms_oms
    and not user_known_write_below_binary_dir_activities
  output: >
    CRITICAL File below a known binary directory opened for writing (user=%user.name file_updated=%fd.name command=%proc.cmdline)
  priority: ERROR
  tags: [filesystem, mitre_persistence]
```

```
vim  /etc/falco/falco.yaml
...
file_output:
  enabled: true
  keep_alive: false
  filename: /opt/security_incidents/alerts.log
...

systemctl restart falco
```
