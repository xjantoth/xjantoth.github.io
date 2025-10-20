---
title: "Kubernetes RBAC"
date: 2022-02-24T10:35:03+0100
lastmod: 2022-02-24T10:35:03+0100
draft: false
description: "Kubernetes RBAC"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['kubernetes', 'rbac']
---

There are namespaced and non namespaced resources in Kubernetes.

* Role (namespaced)              -> RoleBinding
* ClusterRole (non namespaced)   -> ClusterRoleBinding

Be extra careful with `ClusterRole` and `ClusterRoleBinding` because these are not only assigned to currently existing namespaces but also to namespaces created in **future**.


Valid combinations:

1. Role -> RoleBinding
2. ClusterRole -> ClusterRoleBinding
3. ClusterRole -> RoleBinding


Make sure that user **Jane** can only read secretes in namespace **red**.

```yaml
# Create role secret-manager in namespace red to be able to get secrets
k create role -n red secret-manager --verb get --resource secrets -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: red
  creationTimestamp: null
  name: secret-manager
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get

# Create rolebinding to associate a role with a user "jane"
k create rolebinding -n red secret-manager --role=secret-manager --user=jane -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: secret-manager
  namespace: red
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secret-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane

```

Make sure that user **Jane** can only `list, get` secretes in namespace **blue**.


```yaml
k create role -n blue secret-manager --verb=get,list --resource secrets -o
yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: secret-manager
  namespace: blue
rules:
- apiGroups:
  - ""
  resources:
  - secrets
  verbs:
  - get
  - list

# Create rolebinding to associate a role with a user "jane" in blue namespace
k create rolebinding -n blue secret-manager --role=secret-manager --user=jane -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: secret-manager
  namespace: blue
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: secret-manager
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane
```

Test roles and rolebindings

```
k -n red auth can-i list secrets --as jane
no
```

Create and test `ClusterRole` named **deploy-deleter** which allows to delete deployments
1. User "jane" can delete deployments in all namespaces
2. User "jim" can delete deployments only in namespace red


```yaml
# Create and test `ClusterRole` named **deploy-deleter** which allows to delete deployments
k create clusterrole deploy-deleter --verb delete --resource deployment -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: null
  name: deploy-deleter
rules:
- apiGroups:
  - apps
  resources:
  - deployments
  verbs:
  - delete

# 1. User "jane" can delete deployments in all namespaces
k create clusterrolebinding deploy-deleter --clusterrole deploy-deleter --user jane -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  creationTimestamp: null
  name: deploy-deleter
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: deploy-deleter
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jane

# 2. User "jim" can delete deployments only in namespace red
k create rolebinding -n red deploy-deleter --clusterrole deploy-deleter --user jim -o yaml --dry-run=client
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: deploy-deleter
  namespace: red
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: deploy-deleter
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: jim

```

Test clusterrole and clusterrolebinding/rolebindings

```
k -n kube-system auth can-i delete deployment --as jane
yes
k -n red auth can-i delete deployment --as jim
yes

```

There are two kind of accounts in Kubenretes:

* ServiceAccounts
* "normal users" (need to issue a certificate)

![Image](/assets/images/blog/rbac-1.png)

There is no k8s User resource in Kubenretes

![Image](/assets/images/blog/rbac-2.png)

The idea behind issuing a certificate to a user e.g. jane

There is no way to **invalidate** a certificate
If a certificate has been leaked:

* remove all access via RBAC
* username cannot be used intil certificate would expire
* create new CA and re-issue all certificates

![Image](/assets/images/blog/rbac-3.png)

How to issue a certificate for a normal user "jane"

![Image](/assets/images/blog/rbac-4.png)


```
# Generate a private key
openssl genrsa -out jane.key 2048

# Generate a CSR :)
openssl req -new -key jane.key -out jane.csr
...
-----
Country Name (2 letter code) []:
State or Province Name (full name) []:
...
Common Name (eg, fully qualified host name) []:jane
...
to be sent with your certificate request
A challenge password []:

```



```yaml
---
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: jane
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZVzVuWld4aE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQTByczhJTHRHdTYxakx2dHhWTTJSVlRWMDNHWlJTWWw0dWluVWo4RElaWjBOCnR2MUZtRVFSd3VoaUZsOFEzcWl0Qm0wMUFSMkNJVXBGd2ZzSjZ4MXF3ckJzVkhZbGlBNVhwRVpZM3ExcGswSDQKM3Z3aGJlK1o2MVNrVHF5SVBYUUwrTWM5T1Nsbm0xb0R2N0NtSkZNMUlMRVI3QTVGZnZKOEdFRjJ6dHBoaUlFMwpub1dtdHNZb3JuT2wzc2lHQ2ZGZzR4Zmd4eW8ybmlneFNVekl1bXNnVm9PM2ttT0x1RVF6cXpkakJ3TFJXbWlECklmMXBMWnoyalVnald4UkhCM1gyWnVVV1d1T09PZnpXM01LaE8ybHEvZi9DdS8wYk83c0x0MCt3U2ZMSU91TFcKcW90blZtRmxMMytqTy82WDNDKzBERHk5aUtwbXJjVDBnWGZLemE1dHJRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBR05WdmVIOGR4ZzNvK21VeVRkbmFjVmQ1N24zSkExdnZEU1JWREkyQTZ1eXN3ZFp1L1BVCkkwZXpZWFV0RVNnSk1IRmQycVVNMjNuNVJsSXJ3R0xuUXFISUh5VStWWHhsdnZsRnpNOVpEWllSTmU3QlJvYXgKQVlEdUI5STZXT3FYbkFvczFqRmxNUG5NbFpqdU5kSGxpT1BjTU1oNndLaTZzZFhpVStHYTJ2RUVLY01jSVUyRgpvU2djUWdMYTk0aEpacGk3ZnNMdm1OQUxoT045UHdNMGM1dVJVejV4T0dGMUtCbWRSeEgvbUNOS2JKYjFRQm1HCkkwYitEUEdaTktXTU0xMzhIQXdoV0tkNjVoVHdYOWl4V3ZHMkh4TG1WQzg0L1BHT0tWQW9FNkpsYWFHdTlQVmkKdjlOSjVaZlZrcXdCd0hKbzZXdk9xVlA3SVFjZmg3d0drWm89Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth


:read ! cat jane.csr | base64 | tr -d "\n"

```

Then save the content above and `kubectl create -f ...`


```
k create -f  csr.yaml
certificatesigningrequest.certificates.k8s.io/jane created
saq4a@W0188FMI173 blog % k get csr
NAME   AGE   SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
jane   3s    kubernetes.io/kube-apiserver-client   kubernetes-admin   24h                 Pending
```

Approve CertificateSigningRequest


```yaml
k certificate approve jane
certificatesigningrequest.certificates.k8s.io/jane approved
saq4a@W0188FMI173 blog % k get csr
NAME   AGE     SIGNERNAME                            REQUESTOR          REQUESTEDDURATION   CONDITION
jane   6m52s   kubernetes.io/kube-apiserver-client   kubernetes-admin   24h                 Approved,Issued
```

Extract TLS certificate


```
kubectl get csr jane -o jsonpath='{.status.certificate}'| base64 -d  > jane.crt
```

Now, we need to setup **context** in KUBECONFIG


```
k config view
k config set-credentials jane --client-key=jane.key --client-certificate=jane.crt --embed-certs
k config set-context jane --user jane --cluster kubernetes
k config use-context jane

# Now it is up to you setup proper RBAC to grant certain permissions to user "jane"
k get secrets -n blue
NAME                  TYPE                                  DATA   AGE
default-token-nlxct   kubernetes.io/service-account-token   3      3d21h

k get secrets
Error from server (Forbidden): secrets is forbidden: User "jane" cannot list resource "secrets" in API group "" in the namespace "default"

```


1. There are existing Namespaces ns1 and ns2.
Create ServiceAccount pipeline in both Namespaces.
These SAs should be allowed to view almost everything in the whole cluster. You can use the default ClusterRole view for this.
These SAs should be allowed to create and delete Deployments in Namespaces ns1 and ns2.
Verify everything using kubectl auth can-i.

```
k create sa pipeline -n ns1
k create sa pipeline -n ns2

kubectl create clusterrolebinding pipeline-ns1 --clusterrole=view --serviceaccount=ns1:pipeline
kubectl create clusterrolebinding pipeline-ns2 --clusterrole=view --serviceaccount=ns2:pipeline

kubectl create clusterrole deleter --verb=create,delete --resource=deployments

kubectl create rolebinding -n ns1 dele-11 --serviceaccount=ns1:pipeline --clusterrole=deleter
kubectl create rolebinding -n ns2 dele-22 --serviceaccount=ns2:pipeline --clusterrole=deleter

# namespace ns1 deployment manager
k auth can-i delete deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i create deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i update deployments --as system:serviceaccount:ns1:pipeline -n ns1 # NO
k auth can-i update deployments --as system:serviceaccount:ns1:pipeline -n default # NO

# namespace ns2 deployment manager
k auth can-i delete deployments --as system:serviceaccount:ns2:pipeline -n ns2 # YES
k auth can-i create deployments --as system:serviceaccount:ns2:pipeline -n ns2 # YES
k auth can-i update deployments --as system:serviceaccount:ns2:pipeline -n ns2 # NO
k auth can-i update deployments --as system:serviceaccount:ns2:pipeline -n default # NO

# cluster wide view role
k auth can-i list deployments --as system:serviceaccount:ns1:pipeline -n ns1 # YES
k auth can-i list deployments --as system:serviceaccount:ns1:pipeline -A # YES
k auth can-i list pods --as system:serviceaccount:ns1:pipeline -A # YES
k auth can-i list pods --as system:serviceaccount:ns2:pipeline -A # YES
k auth can-i list secrets --as system:serviceaccount:ns2:pipeline -A # NO (default view-role doesn't allow)
```


2. Manually sign the CSR with the K8s CA file to generate the CRT at /root/60099.crt.
Create a new context for kubectl named 60099@internal.users which uses this CRT to connect to K8s.

```
# my solution
openssl genrsa -out /root/60099.key 2048
openssl req -new -key /root/60099.key -out /root/60099.csr


# Official explainations
openssl x509 -req -in 60099.csr -CA /etc/kubernetes/pki/ca.crt -CAkey /etc/kubernetes/pki/ca.key -CAcreateserial -out 60099.crt -days 500
k config set-credentials 60099@internal.users --client-key=60099.key --client-certificate=60099.crt
k config set-context 60099@internal.users --cluster=kubernetes --user=60099@internal.users
k config get-contexts
k config use-context 60099@internal.users
k get ns # fails because no per
```

3. Setup suer 60099 via API CSR


```
openssl genrsa -out /root/60099.key 2048
openssl req -new -key /root/60099.key -out /root/60099.csr

...

k certificate approve userx
k get certificatesigningrequests.certificates.k8s.io userx -o jsonpath='{.status.certificate}' | base64 -d > 60099.crt
k config set-credentials 60099@internal.users --client-key=60099.key --client-certificate=60099.crt --embed-certs
k config set-context 60099@internal.users@kubernetes --cluster=kubernetes --user=60099@internal.users
k config use-context 60099@internal.users@kubernetes
k config current-context
k config get-contexts
k get ns
```
