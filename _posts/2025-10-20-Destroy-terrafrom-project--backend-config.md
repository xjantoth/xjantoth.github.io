---
title: "Destroy Terraform project -backend-config"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
description: "Terraform: Destroy Terraform project -backend-config — HCL examples and best practices."

tags: ['ml', 'terraform', 'backend', 'aws']
categories: ["Terraform"]
---

```
export AWS_SECRET_ACCESS_KEY="..."
export AWS_ACCESS_KEY_ID="..."
export AWS_DEFAULT_REGION="us-west-2"
export TF_VAR_project_name=hruska
cd terraform/k3s
terraform init -backend-config="path=/home/jantoth/Documents/sbx/ml/data/hruska/terraform.tfstate"
terraform destroy
```
