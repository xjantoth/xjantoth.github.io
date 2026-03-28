---
title: "CKS Istio notes"
date: 2022-08-12T18:22:24+0200
lastmod: 2022-08-12T18:22:24+0200
draft: false
description: "Notes on installing Istio service mesh with Kiali, Grafana, and Jaeger on a Kubernetes cluster, including Gateway and VirtualService configuration."
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['cks', 'istio', 'notes']
categories: ["Kubernetes"]
---

#### Work in progress on Istio

Do not forget to restart CoreDNS after you install Calico since there was already a basic CNI activated.

The following commands set up Istio on the cluster: remove taints from the node, deploy a test nginx pod, install Istio and its addons (Kiali, Prometheus, Grafana, Jaeger), enable sidecar injection, and deploy the Google microservices demo.

```bash
k get nodes tf-srv-vibrant-khayyam  -o jsonpath='{.spec.taint}'
k taint node tf-srv-zealous-jepsen node-role.kubernetes.io/master-
k run nginx --image=nginx:alpine --port 80 --expose
k edit svc nginx
curl -L https://istio.io/downloadIstio | sh -
cp istio-1.14.3/bin/istioctl /usr/local/bin/
istioctl isntall
kubectl apply -f istio-1.14.3/samples/addons/kiali.yaml
kubectl apply -f istio-1.14.3/samples/addons/prometheus.yaml
k delete pod -n kube-system coredns-64897985d-9 coredns-64897985d-zk2nj
k delete pod -n kube-system coredns-64897985d-9nqlw coredns-64897985d-t7mz9
kubectl label namespace default istio-injection=enabled
k create -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/main/release/kubernetes-manifests.yaml
k apply -f istio-1.14.3/samples/addons/grafana.yaml
k apply -f istio-1.14.3/samples/addons/jaeger.yaml
k apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/microservices-demo/main/release/istio-manifests.yaml
k get gateways.networking.istio.io -A
k get virtualservices.networking.istio.io
k edit virtualservices.networking.istio.io frontend
k edit virtualservices.networking.istio.io frontend-ingress
k delete virtualservices.networking.istio.io frontend
~
```


#### Gateway and Virtual Service

The following manifest defines an Istio Gateway that accepts HTTP and HTTPS traffic, along with multiple VirtualService resources that route traffic to different backend services based on the hostname.

```yaml
---
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: service-gateway
spec:
  selector:
    istio: ingressgateway # use Istio default gateway implementation
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    hosts:
    - "*"
    tls:
      mode: PASSTHROUGH
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: kiali-ingress
spec:
  hosts:
  - "kiali.vl.k8s"
  gateways:
  - service-gateway
  http:
  - route:
    - destination:
        host: kiali.istio-system.svc.cluster.local
        port:
          number: 20001
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: argocd-ingress
spec:
  hosts:
  - "argocd.vl.k8s"
  gateways:
  - service-gateway
  tls:
  - match:
    - sniHosts:
      - "argocd.vl.k8s"
    route:
    - destination:
        host: argocd-server.argocd.svc.cluster.local
        port:
          number: 443
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: frontend-ingress
spec:
  hosts:
  - "frontend.vl.k8s"
  gateways:
  - service-gateway
  http:
  - route:
    - destination:
        host: frontend.default.svc.cluster.local
        port:
          number: 80
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: grafana-ingress
spec:
  hosts:
  - "grafana.vl.k8s"
  gateways:
  - service-gateway
  http:
  - route:
    - destination:
        host: grafana.istio-system.svc.cluster.local
        port:
          number: 3000
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: nginx-ingress
spec:
  hosts:
  - "nginx.vl.k8s"
  gateways:
  - service-gateway
  http:
  - route:
    - destination:
        host: nginx.default.svc.cluster.local
        port:
          number: 80
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: nginx-ingress
spec:
  hosts:
  - "tracing.vl.k8s"
  gateways:
  - service-gateway
  http:
  - route:
    - destination:
        host: tracing.istio-system.svc.cluster.local
        port:
          number: 80

```
