---
title: "Kubernetes network policies"
date: 2022-01-17T10:14:38+01:00
lastmod: 2022-01-17T10:14:46+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Kubernetes network policies"

tags: ['kubernetes', 'network', 'policies']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


Here is an example of network policies


![Image](/assets/images/blog/np-1.png)

```
k taint node scw-k8s-cks node-role.kubernetes.io/master-
k run frontend --image=nginx
k run backend --image=nginx
k get pods
k expose  pod frontend --port 80
k expose  pod backend --port 80
k get svc
```
If pods has more "network policies" - all of them will be merged.

#### Default deny network policy

```
root@scw-k8s-cks:~# cat default-deny.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-policy
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

# connection does not work anymore
root@scw-k8s-cks:~# k exec frontend -- curl backend
root@scw-k8s-cks:~# k exec backend -- curl frontend
```

#### Setting up following network policies

![Image](/assets/images/blog/np-2.png)


There are two pods currently running at your cluster

```
root@scw-k8s-cks:~# k get pods
NAME       READY   STATUS    RESTARTS   AGE
backend    1/1     Running   0          4h27m
frontend   1/1     Running   0          4h30m
```


#### Frontend part

```yaml
root@scw-k8s-cks:~# cat allow-frontend-to-talk-to-backend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: frontend-talk-to-backend
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: frontend
  policyTypes:
  - Egress
  egress:
  - to:
    - podSelector:
        matchLabels:
          run: backend
    ports:
    - protocol: TCP
      port: 80
```

### Backend part

```yaml
root@scw-k8s-cks:~# cat backend-to-frontend.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-frontend
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: backend
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          run: frontend
    ports:
    - protocol: TCP
      port: 80
```

### Now check wheter we can connect from frontend -> backend

```
root@scw-k8s-cks:~# k get pods -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP          NODE          NOMINATED NODE   READINESS GATES
backend    1/1     Running   0          23h   10.32.0.5   scw-k8s-cks   <none>           <none>
frontend   1/1     Running   0          23h   10.32.0.4   scw-k8s-cks   <none>           <none>
root@scw-k8s-cks:~# k exec -it frontend -- curl 10.32.0.5
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
</html>
```

### Please notice that a direction from backend -> frontend does not work (as it suppose to be)

```
root@scw-k8s-cks:~# k exec -it backend -- curl 10.32.0.4
...
# times out ...
```


### One more extended use case with connection to cassandra database

![Image](/assets/images/blog/np-3.png)

```
root@scw-k8s-cks:~# k create namespace namespace-cassandra
namespace/namespace-cassandra created

# create a label on pod <- this is not needed but it's good to see how to add label and remove label from a POD
root@scw-k8s-cks:~# k label pod --namespace namespace-cassandra cassandra ns=cassandra
pod/cassandra labeled
root@scw-k8s-cks:~# k label pod --namespace namespace-cassandra cassandra ns-


# create a label on a namespace
root@scw-k8s-cks:~# k label namespace namespace-cassandra ns=cassandra
namespace/namespace-cassandra labeled

# check labels
root@scw-k8s-cks:~# k get ns namespace-cassandra --show-labels
NAME                  STATUS   AGE   LABELS
namespace-cassandra   Active   12m   kubernetes.io/metadata.name=namespace-cassandra,ns=cassandra

root@scw-k8s-cks:~# k expose pod --namespace namespace-cassandra cassandra --port 80
service/cassandra exposed

# Check cassandra IPv4 address
root@scw-k8s-cks:~# k get pods -o wide -n namespace-cassandra
NAME        READY   STATUS    RESTARTS   AGE   IP          NODE          NOMINATED NODE   READINESS GATES
cassandra   1/1     Running   0          30m   10.32.0.6   scw-k8s-cks   <none>           <none>

```

##### Create one more policy

```
iroot@scw-k8s-cks:~# cat backend-to-cassandra.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-cassandra
  namespace: default
spec:
  podSelector:
    matchLabels:
      run: backend
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          ns: cassandra
    ports:
    - protocol: TCP
      port: 80


k create -f backend-to-cassandra.yaml
```
##### Check connection from backend to Cassandra


```
root@scw-k8s-cks:~# k exec backend -- curl http://10.32.0.6
<!DOCTYPE html>
<html>
<head>
...
</body>
</html>
root@scw-k8s-cks:~#
```

##### Make it more complex - create default deny in namespace-cassandra to block all traffic

```
root@scw-k8s-cks:~# cat default-deny-cassandra.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cassandra-deny-policy
  namespace: namespace-cassandra
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

k create -f default-deny-cassandra.yaml
```

Now, connection between backend and cassandra does not work anymore.

```
root@scw-k8s-cks:~# k exec backend -- curl http://10.32.0.6

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0^C
```


```
# Create a new label on default namespace
root@scw-k8s-cks:~# k label namespaces default ns=default
namespace/default labeled


# Create a new network policy for Ingress at pod cassandra
root@scw-k8s-cks:~# cat from-backend-to-cassandra.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-to-cassandra
  namespace: namespace-cassandra
spec:
  podSelector:
    matchLabels:
      run: cassandra
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          ns: default

k create -f from-backend-to-cassandra.yaml
```

##### Check the connection now from backend to cassandra

```
root@scw-k8s-cks:~# k exec backend -- curl http://10.32.0.6
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   615  100   615    0     0   200k      0 --:--:-- --:--:-- --:--:--  200k
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```


##### Allow DNS 53 from default namespace

```
cat <<EOF > allow-dns-np.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  - Ingress
  egress:
  - ports:
    - port: 53
      protocol: TCP
    - port: 53
      protocol: UDP
EOF
```

##### There are existing Pods in Namespace app.

We need a new default-deny NetworkPolicy named deny-out for all outgoing traffic of these Pods.
It should still allow DNS traffic on port 53 TCP and UDP.

```
cat np.yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-out
  namespace: app
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    ports:
    - protocol: TCP
      port: 53
    - protocol: UDP
      port: 53
```
