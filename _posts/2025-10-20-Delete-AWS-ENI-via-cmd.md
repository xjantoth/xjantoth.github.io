---
title: "Delete AWS ENI via cmd"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/aws-1.jpg"
description: "Delete AWS ENI via cmd"

tags: ['delete', 'aws', 'eni', 'via', 'cmd']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
echo $t
error waiting for EKS Node Group (eks-mlflow:eks-mlflow-cpu-ng) deletion: Ec2SecurityGroupDeletionFailure: DependencyViolation - resource has a dependent object. Resource IDs: [sg-00db6bb5ee949a63c]

echo $t | sed -E 's/^(.*\[)(.*)(\])$/\2/'

aws ec2 describe-network-interfaces --profile jan-toth-ml | jq -r ".NetworkInterfaces[] | select(.Description | startswith(\"aws-K8S-i-\")) | .NetworkInterfaceId"

```
