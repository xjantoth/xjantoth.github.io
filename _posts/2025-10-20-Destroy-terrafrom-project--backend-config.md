---
title: "Destroy Terraform project with -backend-config"
date: "2022-01-07T11:48:59+0100"
lastmod: "2022-01-07T11:48:59+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
description: "How to destroy a Terraform project using a custom backend-config path for the state file."

tags: ['ml', 'terraform', 'backend', 'aws']
categories: ["Terraform"]
---

To destroy a Terraform-managed infrastructure when the state file is stored at a custom local path, first set your AWS credentials as environment variables, then run `terraform init` with the `-backend-config` flag pointing to the state file location, and finally run `terraform destroy`.

```bash
export AWS_SECRET_ACCESS_KEY="..."
export AWS_ACCESS_KEY_ID="..."
export AWS_DEFAULT_REGION="us-west-2"
export TF_VAR_project_name=hruska
cd terraform/k3s
terraform init -backend-config="path=/home/jantoth/Documents/sbx/ml/data/hruska/terraform.tfstate"
terraform destroy
```
