---
title: "AWS EKS aws-auth configmap mapUsers"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-1.jpg"
description: "AWS EKS aws-auth configmap mapUsers"

tags: ["kubernetes", "aws", "eks"]
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Take a backup of ''aws-auth'' config map in ''kube-system'' namespace

```
kubectl get cm aws-auth -n kube-system -o yaml > aws-auth.yaml
```

##  Create file ''aws-auth.yaml'' with proper AWS users

```
cat > aws-auth.yaml <<'EOF'
apiVersion: v1
data:
  mapRoles: |
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::111222333444:role/eks-cluster-node-group-tf
      username: system:node:{{EC2PrivateDNSName}}
  mapUsers: |
    - userarn: arn:aws:iam::111222333444:root
      username: root
      groups:
        - system:masters
    - userarn: arn:aws:iam::111222333444:user/jan.toth
      username: jan.toth
      groups:
        - system:masters
    - userarn: arn:aws:iam::111222333444:user/test.user
      username: test.user
      groups:
        - system:masters

kind: ConfigMap
metadata:
  name: aws-auth
  namespace: kube-system
EOF

kubectl apply -f  aws-auth.yaml
```

##  Update your local ''KUBECONFIG'' file

```
unset KUBECONFIG
export AWS_PROFILE=test-user-ml
aws eks --region us-west-2  update-kubeconfig --name x-ml-eks --profile test-user-ml
```

##  ''Verify'' whether you can access the AWS EKS cluster as the ''user'' who ''did not'' create EKS via ''terrafrom''

```
 kubectl get pods -A
NAMESPACE     NAME                       READY   STATUS    RESTARTS   AGE
kube-system   aws-node-fhjcr             1/1     Running   0          43m
kube-system   aws-node-lm226             1/1     Running   0          43m
kube-system   coredns-5946c5d67c-b7nbj   1/1     Running   0          46m
kube-system   coredns-5946c5d67c-f7dlp   1/1     Running   0          46m
kube-system   kube-proxy-7v65s           1/1     Running   0          43m
kube-system   kube-proxy-xftx8           1/1     Running   0          43m

```
