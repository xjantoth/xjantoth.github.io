---
title: "How to convert yaml variable file for terraform to native hcl tfvars"
date: 2026-02-25T14:15:53+01:00
lastmod: 2026-02-25T14:15:53+01:00
draft: false
description: "How to convert a YAML variable file for Terraform to native HCL tfvars format using yq, jq, and json2hcl."
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: []
categories: ["Terraform"]
---

If there is ever a need to convert a YAML variable file for Terraform to native HCL tfvars format, you can
use the following approach.

First, install the `json2hcl` tool via Homebrew. Then pipe the YAML file through `yq` to convert it to JSON, use `jq` to extract the relevant section, and finally pass it through `json2hcl` to produce HCL output.

```bash
brew install json2hcl
cat data/prod/root.yaml | yq -ojson | jq .azure_secret_engines | json2hcl
```
