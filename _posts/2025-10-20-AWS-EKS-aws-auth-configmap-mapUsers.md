---
title: "AWS EKS aws-auth configmap mapUsers"
date: "2022-01-07T11:30:42+0100"
lastmod: "2022-01-07T11:30:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1667372393119-3d4c48d07fc9?w=800&h=420&fit=crop"
description: "How to manage the aws-auth ConfigMap in EKS to grant IAM users access to the Kubernetes cluster, including backup, editing, and verification steps."

tags: ['kubernetes', 'aws', 'eks']
categories: ["Kubernetes"]
---

## Take a backup of the aws-auth ConfigMap in kube-system namespace

Before making any changes to the `aws-auth` ConfigMap, always take a backup. This ConfigMap controls which IAM roles and users can access the EKS cluster.

```bash
kubectl get cm aws-auth -n kube-system -o yaml > aws-auth.yaml
```

## Create the aws-auth.yaml file with proper AWS users

The following command creates an `aws-auth` ConfigMap that maps IAM roles (for node groups) and IAM users to Kubernetes RBAC groups. This allows specific AWS users to authenticate to the EKS cluster.

```yaml
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

## Update your local KUBECONFIG file

After updating the `aws-auth` ConfigMap, refresh your local kubeconfig so that kubectl uses the correct AWS profile and cluster endpoint.

```bash
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
