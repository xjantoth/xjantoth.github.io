---
title: "CKS serviceaccount"
date: 2022-03-07T12:57:03+0100
lastmod: 2022-03-07T12:57:03+0100
draft: false
description: "CKS serviceaccount"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'serviceaccount']
---

* SesrviceAccount (SA) are namespaces
* SA "default" in every namespace automatically mounted to a pod
* can be used to talk to Kubernetes API


```
k create sa accessor
k run accessor --image=nginx:alpine -o yaml --dry-run=client > accessor.yaml

vim accessor.yaml
...
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: accessor
  name: accessor
spec:
  serviceAccount: accessor   # < --- adding this line
  containers:
  - image: nginx:alpine
    name: accessor
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

...
:wq!

k create -f accessor.yaml

```


Let's elaborate a bit on what has been done so far by getting inside of a newly created pod called "accessor"



```
# Get inside a pod
k exec -it accessor -- sh

/ # cat  /run/secrets/kubernetes.io/serviceaccount/token
eyJhbGciOiJSUzI1NiIsImtpZCI6IlZPVUZEc3oyNldBeTZmcWpneW53bmNjWUVqNElKV05adGdjbTlaQlBySEkifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiXSwiZXhwIjoxNjc4MTkwNzIyLCJpYXQiOjE2NDY2NTQ3MjIsImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJkZWZhdWx0IiwicG9kIjp7Im5hbWUiOiJhY2Nlc3NvciIsInVpZCI6ImNjNzljYTQwLWQ2ZjMtNDJiNy05ZTZmLTU3NjhiYWUwZTc3MiJ9LCJzZXJ2aWNlYWNjb3VudCI6eyJuYW1lIjoiYWNjZXNzb3IiLCJ1aWQiOiI5YzIyODU4Zi1hZDNlLTRhMzMtYTU1MC1mMzJiMTY1YWJmZTUifSwid2FybmFmdGVyIjoxNjQ2NjU4MzI5fSwibmJmIjoxNjQ2NjU0NzIyLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6ZGVmYXVsdDphY2Nlc3NvciJ9.XBaD1eIZ9BJ5MyRgJw2pf3cNhN_oHK3g_ipPTUp_mW2egr-AOt4whCyb9hmIOrGyYsBb-R4Lo3obiSoPasS4kETzocQPFKksGwz4hVANaxcNIA0oHo_TDwRLBH4aA4P3mqHV6ku4fyBobDxzdaT77tF9zlvs4yBwM97-wvbYMudfvaxGdD_X6NwrnVvefIxraPJORQ2IJbLuaQTulOXYde-XE692PJZV5IM4aCHGmloGcCTSEs23ykNyLTK4mZLj4BZCm3WFMNgiG1oXXJ4FjFBnaA-cCT229cWB7QJ1MMcl8nFY0bvRdfhGm8zP71Bm7kDuLewyYQmt6TomvaUaYg/
```


Let's try to call Kubenretes API from inside of a pod


```
/ # curl https://kubernetes -k
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}
```

Hmmm, it is forbidden for anonymous user as it can be see above. How about passing a bearer token within a curl request. Give it a try.


```
/ # curl https://kubernetes -k -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceacc
ount/token)"
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "forbidden: User \"system:serviceaccount:default:accessor\" cannot get path \"/\"",
  "reason": "Forbidden",
  "details": {},
  "code": 403
}
```

Ok, still not much of an success but do not give up and go on


```
/ # curl https://kubernetes/api -X GET -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/se
rviceaccount/token)" --cacert /run/secrets/kubernetes.io/serviceaccount/ca.crt
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "192.168.5.15:6443"
    }
  ]
}
```


Let's figure out how to get list of all pods running in a default namespace


```
/ # curl https://kubernetes/api/v1/namespaces/default/pods/ -X GET -H "Authorization: Bearer $(cat /
run/secrets/kubernetes.io/serviceaccount/token)" --cacert /run/secrets/kubernetes.io/serviceaccount/
ca.crt
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "pods is forbidden: User \"system:serviceaccount:default:accessor\" cannot list resource \"pods\" in API group \"\" in the namespace \"default\"",
  "reason": "Forbidden",
  "details": {
    "kind": "pods"
  },
  "code": 403
}/ #

```

Hmmm it looks like we do not have permissions to list pods at all. We will create role and rolebinding and try it again.


```
% k create role pod-reader -n default --verb list --resource pods

% k create rolebinding pod-reader-rb -n default --serviceaccount default:accessor --role pod-reader

/ # curl -s https://kubernetes/api/v1/namespaces/default/pods/ -X GET -H "Authorization: Bearer $(cat /run/secrets/kubernetes.io/serviceaccount/token)" --cacert /run/secrets/kubernetes.io/serviceaccount/ca.crt| jq '.items[].metadata.name'
"accessor"
"httpd1"
"nginx1"
"serverrr"

...

```

There is one special option for SesrviceAccount in general called **automountServiceAccountToken**.

Let's try to disable SesrviceAccount token to be moounted to pod.


```
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: accessor
  name: accessor
spec:
  automountServiceAccountToken: false # < --- add this line
  # serviceAccount: accessor
  containers:
  - image: nginx:alpine
    name: accessor
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

```

Once configuration above is specified - there is not `/run/secrets` folder present anymore


Now, let's see if we can delete `secrets` as serviceaccount **accessor**


```
k auth can-i delete secrets --as system:serviceaccount:default:accessor
no
```

How about now?


```
k create clusterrolebinding accessor-default
-edit --clusterrole edit --serviceaccount default:accessor
clusterrolebinding.rbac.authorization.k8s.io/accessor-default-edit created
k auth can-i delete secrets --as system:serviceaccount:default:accessor
yes

```
