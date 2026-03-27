---
title: "How to convert yaml variable file for terraform to native hcl tfvars"
date: 2026-02-25T14:15:53+01:00
lastmod: 2026-02-25T14:15:53+01:00
draft: false
description: "If there is ever a need to convert yaml variable file for terraform to native hcl tfvars, one can use this command."
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: []
categories: ["Terraform"]
---

If there is ever a need to convert yaml variable file for terraform to native hcl tfvars, one can 
use this command.

```bash
brew install json2hcl
cat data/prod/root.yaml| yq -ojson | jq .azure_secret_engines | json2hcl
```
