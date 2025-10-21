---
title: "Game of Pods - Tyro"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Game of Pods - Tyro"

tags: ['game', 'pods', 'tyro']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
kubectl config set-context --current --cluster=kubernetes  --namespace=development --user=drogo

kubectl config use-context developer --cluster=kubernetes  --namespace=development --user=drogo
kubectl config current-context
```
```
cat ~/.kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0t...VkU2bVFFS2x0cHliUVVFZTRncmY2OGVUbz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
    server: https://172.17.0.61:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    namespace: development
    user: drogo
  name: developer
- context:
    cluster: kubernetes
    namespace: development
    user: drogo
  name: development
- context:
    cluster: kubernetes
    namespace: development
    user: drogo
  name: kubernetes-admin@kubernetes
current-context: developer
kind: Config
preferences: {}
users:
- name: drogo
  user:
    client-certificate: /root/drogo.crt
    client-key: /root/drogo.key
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS...QgQ0VSVElGSUNBVEUtLS0tLQo=
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNS...hVN25LN0xNUkUvRGNPNFJla0VGZEh6SkhVUjB
```

```yaml
 for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
filename: pod.yaml
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  namespace: development
  labels:
    run: jekyll
  name: jekyll
spec:
  volumes:
  - name: site
    persistentVolumeClaim:
      claimName: jekyll-site
  initContainers:
  - name: copy-jekyll-site
    image: kodekloud/jekyll
    command: [ "jekyll", "new", "/site" ]
    volumeMounts:
    - name: site
      mountPath: "/site"
  containers:
  - image: kodekloud/jekyll-serve
    name: jekyll
    resources: {}
    volumeMounts:
    - name: site
      mountPath: "/site"
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}

filename: pvc.yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: jekyll-site
  namespace: development
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi

filename: pv.yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: jekyll-site
spec:
  accessModes:
  - ReadWriteMany
  capacity:
    storage: 1Gi
  hostPath:
    path: /site
    type: ""
  persistentVolumeReclaimPolicy: Retain
  volumeMode: Filesystem
filename: rolebinginf.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  creationTimestamp: null
  name: developer-rolebinding
  namespace: development
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: developer-role
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: drogo
filename: role.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: null
  name: developer-role
  namespace: development
rules:
- apiGroups:
  - ""
  resources:
  - services
  - persistentvolumeclaims
  - pods
  verbs:
  - '*'

filename: svc.yaml
---
apiVersion: v1
kind: Service
metadata:
  labels:
    run: jekyll
  name: jekyll
  namespace: development
spec:
  ports:
  - nodePort: 30097
    port: 8080
    protocol: TCP
    targetPort: 4000
  selector:
    run: jekyll
  type: NodePort
```
