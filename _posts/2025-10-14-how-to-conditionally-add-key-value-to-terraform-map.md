---
title: How to conditionally add key value to Terraform map
date: 2024-06-19T13:25:38+0200
lastmod: 2024-06-19T13:25:38+0200
draft: false
description: "This code will conditionally add or ommit netapp-cleaner block based on prefix local variable."
image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'terraform']
categories: ["Terraform"]
---


This code will conditionally add or ommit `netapp-cleaner` block based on `prefix` local variable.

```tf
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


## Links:

202406191306
