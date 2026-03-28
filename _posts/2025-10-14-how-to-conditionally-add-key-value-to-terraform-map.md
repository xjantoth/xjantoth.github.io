---
title: How to conditionally add key value to Terraform map
date: 2024-06-19T13:25:38+0200
lastmod: 2024-06-19T13:25:38+0200
draft: false
description: "This code will conditionally add or omit a netapp-cleaner block based on the prefix local variable using Terraform's merge and ternary operator."
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'terraform']
categories: ["Terraform"]
---


This code will conditionally add or omit the `netapp-cleaner` block based on the `prefix` local variable. It uses Terraform's `merge()` function combined with a ternary expression to include or exclude the extra map entry. When `local.prefix` matches the expected value, the additional block is merged into the map; otherwise, an empty map is merged, effectively omitting it.

```hcl
locals {
  prefix = "deaut"
  raj = merge({
    netapp-admin = {
      member = "serviceAccount:raj",
      role = "roles/netapp.admin"
    },
    netapp-user = {
      member = "serviceAccount:jan",
      role = "roles/netapp.user"
    },

  },
  local.prefix == "xdeaut" ? {
  netapp-cleaner = {
        member = "serviceAccount:cleaner",
        role = "roles/blaaaa"
      }
  }: {}
  )
}
output "debug" {
   value = local.raj
   description = "debug"
}

```


