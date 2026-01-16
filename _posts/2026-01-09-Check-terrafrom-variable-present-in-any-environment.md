---
title: "Check terrafrom variable present in any environment"
date: 2026-01-09T10:45:30:+0100
lastmod: 2026-01-09T10:45:30:+0100
draft: false
description: "Check terrafrom variable present in any environment"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: []
---


```bash
module "wiz" {
  source  = "localterraform.com/modules/wizz/gcp"
  version = "0.1.1"
  for_each = can(var.wizz_settings) && var.wizz_settings.wiz_managed_identity_external_id != null ? {
    for k, v in var.wizz_settings : k => v
  } : {}

  org_id                           = var.organization.id
  wiz_managed_identity_external_id = each.value
  serverless_scanning              = true
  data_scanning                    = true
  enable_shadow_data               = false
  forensic                         = false
}
```
