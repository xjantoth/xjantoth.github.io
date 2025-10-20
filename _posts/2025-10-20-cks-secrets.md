---
title: "CKS secrets"
date: 2022-04-29T11:29:02+0200
lastmod: 2022-04-29T11:29:02+0200
draft: false
description: "CKS secrets"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'secrets']
---


```

k create secret generic secret1 --from-literal=jano=jano
k create secret generic secret2 --from-literal=toth=toth

root@scw-k8s:~# cat pod.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: pod
  name: pod
spec:
  containers:
  - image: nginx:alpine
    env:
      - name: secret2
        valueFrom:
          secretKeyRef:
            name: secret2
            key: toth
            optional: false # same as default; "mysecret" must exist
                            # and include a key named "username"
    volumeMounts:
    - name: secret1
      mountPath: "/etc/secret1"
      readOnly: true
    name: pod
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:
  - name: secret1
    secret:
      secretName: secret1
status: {}
root@scw-k8s:~# k get pods
NAME   READY   STATUS    RESTARTS   AGE
pod    1/1     Running   0          2d1h

```

###### Check if you can access ETCD at master node


```
# Determine TSL components for a connection string
root@scw-k8s:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml  | grep etcd
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379

# Connect to ETCD
root@scw-k8s:~# ETCDCTL=3 etcdctl \
--cacert="/etc/kubernetes/pki/etcd/ca.crt"\
--key="/etc/kubernetes/pki/apiserver-etcd-client.key"\
--cert="/etc/kubernetes/pki/apiserver-etcd-client.crt"\
endpoint health

127.0.0.1:2379 is healthy: successfully committed proposal: took = 148.940998ms
```


###### Let's try to get some data from ETCD


```
# Retrieve information about a pod called "pod" in a default namespace
ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/pods/default/pod

# Retrieve information about a secret called "secret1" in a default namespace
ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/secrets/default/secret1
```

###### Encrypt ETCD secrets via API server at REST

```
# Create folder etcd and touch file encryption-configuration.yaml with a following content
head -c 32 /dev/urandom | base64

mkdir /etc/kubernetes/etcd
cat <<'EOF' > /etc/kubernetes/etcd/encryption-configuration.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: $(head -c 32 /dev/urandom | base64)
      - identity: {}
EOF

# Adjust kube-apiserver with --encryption-provider-config flag in kube-apiserver manifest
root@scw-k8s:~# mv  /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
root@scw-k8s:~# vim /tmp/kube-apiserver.yaml

...

  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.18.164.57
    ...
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
    - --encryption-provider-config=/etc/kubernetes/etcd/encryption-configuration.yaml  # <<< add this line
...
    volumeMounts:
    ...
    - mountPath: /etc/kubernetes/etcd
      name: encryption-configuration
      readOnly: true
    ...

  volumes:
  ...
  - hostPath:
      path: /etc/kubernetes/etcd
      type: DirectoryOrCreate
    name: encryption-configuration
  ...


...

root@scw-k8s:~# mv  /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml
```

###### Verifying that data is encrypted


```
kubectl create secret generic secret1 -n default --from-literal=mykey=mydata

# Verify
kubectl describe secret secret3 -n default

ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/secrets/default/secret3

/registry/secrets/default/secret3
k8s:enc:aescbc:v1:key1:W@\ve=2믔%DF٘OBւ̐'~Ym?jH9T%!!,<SkQ܌58DȺys
]/h|ߪ囗kl{뭳uEcW̵"0ɦcڞ?.?@#Ktb2
~x?,Jڇ

```


###### Ensure all Secrets are encrypted


```
kubectl get secrets --all-namespaces -o json | kubectl replace -f -

# Now even secret1 (previously unencrypted) is now encrypted
ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/secrets/default/secret1

/registry/secrets/default/secret1
k8s:enc:aescbc:v1:key1:IP&EmMW)U%5+#ng}HBU1Hڠ7!*0_t
9<ܒc.:FE!78TS\̂Yt?SmC[T
Vc]d]&ǀ#IpKV$&p_9Q|Mۉ<S:/~Miy?%BEB
`ea<VdU*)

```

###### Rotating a decryption key

Changing a Secret without incurring downtime requires a multi-step operation, especially in the presence of a highly-available deployment where multiple kube-apiserver processes are running.

1. Generate a new key and add it as the second key entry for the current provider on all servers
2. Restart all kube-apiserver processes to ensure each server can decrypt using the new key
3. Make the new key the first entry in the keys array so that it is used for encryption in the config
4. Restart all kube-apiserver processes to ensure each server now encrypts using the new key
5. Run kubectl get secrets --all-namespaces -o json | kubectl replace -f - to encrypt all existing Secrets with the new key
6. Remove the old decryption key from the config after you have backed up etcd with the new key in use and updated all Secrets
7. When running a single kube-apiserver instance, step 2 may be skipped.


###### Decrypting all data

Notice that identity is now placed before aescbc

```
vim /etc/kubernetes/etcd/encryption-configuration.yaml

...
root@scw-k8s:~# cat  /etc/kubernetes/etcd/encryption-configuration.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - identity: {}   # <<< Notice that identity is now placed before aescbc !!!
      - aescbc:
          keys:
            - name: key1
              secret: XarzlsSwA+ByS2Ni9RxE1M9m544w52HjZ1Tmc+Z+25M=


...

# Restart kube-apiserver
root@scw-k8s:~# mv  /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/kube-apiserver.yaml

# Wait few seconds until kube-apiserver goes down
root@scw-k8s:~# mv  /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/
```

All secrets are still encrypted at this time!


```
# Now even secret1 (previously unencrypted) is now encrypted
ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/secrets/default/secret1

/registry/secrets/default/secret1
k8s:enc:aescbc:v1:key1:IP&EmMW)U%5+#ng}HBU1Hڠ7!*0_t
9<ܒc.:FE!78TS\̂Yt?SmC[T
Vc]d]&ǀ#IpKV$&p_9Q|Mۉ<S:/~Miy?%BEB
`ea<VdU*)
```

Then run the following command to force decrypt all Secrets:

```
kubectl get secrets --all-namespaces -o json | kubectl replace -f -
```

All secrets has been decrepted


```
ETCDCTL=3 etcdctl \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--key=/etc/kubernetes/pki/apiserver-etcd-client.key \
--cert=/etc/kubernetes/pki/apiserver-etcd-client.crt \
get /registry/secrets/default/secret1
/registry/secrets/default/secret1

k8s
v1Secret

secret1default"*$a519153c-7890-48d9-adf5-acd2f8b8ba662za
kubectl-createUpdatevFieldsV1:-
+{"f:data":{".":{},"f:jano":{}},"f:type":{}}B

janojanoOpaque"

```

###### Filter out all secrets within default namespace of type Opaque


```
root@scw-k8s:~# kubectl get secret -o=jsonpath='{range .items[?(@.type=="Opaque")]}{.kind} {.metadata.name} {.metadata.namespace} {.type}{"\n"}{end}'
Secret secret1 default Opaque
Secret secret2 default Opaque
Secret secret3 default Opaque

```


```
# Create secrets
k create secret generic sec-a1 --from-literal=jano=miso -n ns-secure
k create secret generic sec-a2 --from-file=/etc/hosts -n ns-secure
k run secret-manager -n ns-secure  --image=httpd:alpine -o yaml --dry-run=client > secret-manager.yaml

# Setup pod according an assessment
controlplane $ cat secret-manager.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-manager
  name: secret-manager
  namespace: ns-secure
spec:
  serviceAccount: secret-manager
  containers:
  - image: httpd:alpine
    env:
      - name: SEC_A1
        valueFrom:
          secretKeyRef:
            name: sec-a1
            key: jano
            optional: false # same as default; "mysecret" must exist
    name: secret-manager
    resources: {}
    volumeMounts:
    - name: sec-a2
      mountPath: /etc/sec-a2
      readOnly: true
  dnsPolicy: ClusterFirst
  restartPolicy: Always
  volumes:
  - name: sec-a2
    secret:
      secretName: sec-a2
```
