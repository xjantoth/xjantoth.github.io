---
title: "Kubernetes Ingress"
date: 2022-02-21T13:16:34+01:00
lastmod: 2022-02-21T13:16:38+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Ingress"

tags: ['kubernetes', 'ingress']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

###### Services in Kubernetes

* ClusterIP (points to a pod via labels selectors)
* NodePort (in addition a port is exported at each node)
* Loadbalancer (in addition creates LB at cloud provider)

###### Deploy Nginx ingress controller

```
# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/cluster-setup/secure-ingress/nginx-ingress-controller.yaml
```


```
# Create two different pods in your cluster
k run nginx1 --image=nginx:alpine
k run httpd1 --image=httpd
k expose pod nginx1 --port 80 --name service1 --type ClusterIP
k expose pod httpd1 --port 80 --name service2 --type ClusterIP
```

```yaml

cat <<'EOF' > ingress.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - http:
      paths:
      - path: /service1
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
      - path: /service2
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
EOF
```

####### Test connection

```
k get svc
hugo % k get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP   2d22h
service1     ClusterIP   10.108.141.216   <none>        80/TCP    4m5s
service2     ClusterIP   10.105.255.4     <none>        80/TCP    3m49s

hugo % k get svc -n ingress-nginx
NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
ingress-nginx-controller             NodePort    10.100.237.178   <none>        80:31500/TCP,443:31209/TCP   13m
ingress-nginx-controller-admission   ClusterIP   10.99.183.238    <none>        443/TCP                      13m


curl http://127.0.0.1:31500/service1
curl http://127.0.0.1:31500/service2
```


###### Secure Nginx Ingress with Self Signed Certificate


```

# generate cert & key
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

k create secret tls secure-ingress --cert cert.pem --key key.pem
secret/secure-ingress created



cat <<'EOF' > secure-ingress.yaml
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: secure-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  tls:
  - hosts:
      - secure-ingress.com
    secretName: secure-ingress
  rules:
  - host: secure-ingress.com
    http:
      paths:
      - path: /service1
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
      - path: /service2
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
EOF

# Test connection
curl -k  https://127.0.0.1:31209/service1 -H "Host: secure-ingress.com" #     < --- this will not work !!!
curl -kv  https://secure-ingress.com:31209/service1 --resolve secure-ingress.com:31209:127.0.0.1

...
* TLSv1.2 (IN), TLS change cipher, Change cipher spec (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES128-GCM-SHA256
* ALPN, server accepted to use h2
* Server certificate:
*  subject: C=SK; ST=SK; L=KO; O=Devops; OU=Security; CN=secure-ingress.com
*  start date: Feb 21 12:23:48 2022 GMT
*  expire date: Feb 21 12:23:48 2023 GMT
*  issuer: C=SK; ST=SK; L=KO; O=Devops; OU=Security; CN=secure-ingress.com
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
...

```


# Complete Example
https://github.com/killer-sh/cks-course-environment/tree/master/course-content/cluster-setup/secure-ingress

# K8s Ingress Docs
https://kubernetes.io/docs/concepts/services-networking/ingress
```

######  Ingress object can't be created by kubectl

```yaml
cat ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: app-space
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /watch
        pathType: Prefix
        backend:
          service:
            name: video-service
            port:
              number: 8080
      - path: /wear
        pathType: Prefix
        backend:
          service:
            name: wear-service
            port:
              number: 8080
```

##  Expose already existing deployment with proper namespace

```yaml
kubectl expose deployment ingress-controller --port=80 --target-port=80 --name ingress --type=NodePort --namespace ingress-space --dry-run=client -o yaml | sed -E 's/^(\s*targ.*)/\1\n    nodePort: 30080/' | sed -E 's/^(\s*metadata.*)/\1\n  namespace: ingress-space/'
apiVersion: v1
kind: Service
metadata:
  namespace: ingress-space
  creationTimestamp: null
  name: ingress
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
    nodePort: 30080
  selector:
    name: nginx-ingress
  type: NodePort
status:
  loadBalancer: {}
```

##  !!! Ingress ''cannot'' refer to a service in ''different'' namespace ###
* as such it is important to create ''an ingress'' in the same namespace as the ''service'' resides

```yaml
cat ing.yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  name: ingress-wear-watch
  namespace: app-space
spec:
  rules:
  - http:
      paths:
      - backend:
          serviceName: wear-service
          servicePort: 8080
        path: /wear
        pathType: ImplementationSpecific

      - backend:
          serviceName: video-service
          servicePort: 8080
        path: /watch
        pathType: ImplementationSpecific

      - backend:
          serviceName: video-service
          servicePort: 8080
        path: /stream
        pathType: ImplementationSpecific
```

Examples

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: /pay
        backend:
          serviceName: pay-service
          servicePort: 8282
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
  name: rewrite
  namespace: default
spec:
  rules:
  - host: rewrite.bar.com
    http:
      paths:
      - backend:
          serviceName: http-svc
          servicePort: 80
        path: /something(/|$)(.*)
```

###### Generate SSL certificate and create a kubernetes secret

```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
kubectl  create  secret tls secure-ingress --cert cert.pem --key key.pem
```

Create ''Kubernetes Ingress'' specification

```
cat ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
      - secure-ingress.com
    secretName: secure-ingress
  rules:
  - host: secure-ingress.com
    http:
      paths:
      - path: /service1
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
      - path: /service2
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 80
```

Adjust ''/etc/hosts''

```
echo -e "35.198.101.56 secure-ingress.com" >> /etc/hosts
```

**Check apps'' via curl

```
curl https://secure-ingress.com:30769/service2 -kv
```
