---
title: "Delete AWS ENI via cmd"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
description: "AWS: Delete AWS ENI via cmd — setup and configuration guide."

tags: ['aws', 'eni', 'cmd']
categories: ["AWS"]
---

When deleting an EKS node group, you may encounter a `DependencyViolation` error caused by lingering Elastic Network Interfaces (ENIs). The commands below extract the security group ID from the error message using `sed`, then query the AWS API for all ENIs associated with EKS-managed instances so you can identify and clean them up.

```bash
echo $t
error waiting for EKS Node Group (eks-mlflow:eks-mlflow-cpu-ng) deletion: Ec2SecurityGroupDeletionFailure: DependencyViolation - resource has a dependent object. Resource IDs: [sg-00db6bb5ee949a63c]

echo $t | sed -E 's/^(.*\[)(.*)(\])$/\2/'

aws ec2 describe-network-interfaces --profile jan-toth-ml | jq -r ".NetworkInterfaces[] | select(.Description | startswith(\"aws-K8S-i-\")) | .NetworkInterfaceId"

```
