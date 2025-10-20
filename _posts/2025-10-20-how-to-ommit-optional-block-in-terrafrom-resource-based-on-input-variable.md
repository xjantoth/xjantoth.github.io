---
title: "How to ommit optional block in terrafrom resource based on input variable"
date: 2022-08-19T09:36:10+0200
lastmod: 2022-08-19T09:36:10+0200
draft: false
description: "How to ommit optional block in terrafrom resource based on input variable"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - ommit
  - optional
  - block
  - terraform
---

The goal is to create azurerm_virtual_hub_connection which might or might not have an optional block called `static_vnet_route` section under `routing {}` block.

File `variables.tf`


```
variable "static_vnet_routes" {
  description = "Static routes for virtual network connection"
  type        = list(any)
  default     = []
}
```

File `terrafrom.tfvars`

```
static_vnet_routes = [
    #{
    #  name = "static_route_1"
    #  address_prefixes = ["10.0.2.0/24"]
    #  next_hop_ip_address = "10.0.1.2"
    #},
    #{
    #  name = "static_route_2"
    #  address_prefixes = ["10.0.3.0/24"]
    #  next_hop_ip_address = "10.0.1.4"
    #}
]
```

And finally `azurerm_virtual_hub_connection` resource looks like following:


```
resource "azurerm_virtual_hub_connection" "vhub_connection" {
  name                      = var.vhub_connection_name
  virtual_hub_id            = var.virtual_hub_id
  remote_virtual_network_id = azurerm_virtual_network.vnet.id
  routing {
      # static_vnet_route {}
      dynamic "static_vnet_route" {
        for_each = length(var.static_vnet_routes) > 0 ? var.static_vnet_routes : tolist(
          [
            {
              name = null
              address_prefixes = null
              next_hop_ip_address = null
            }
          ]
        )
        iterator = static_route
        content {
          name                = static_route.value.name
          address_prefixes    = static_route.value.address_prefixes
          next_hop_ip_address = static_route.value.next_hop_ip_address
        }
      }
  }
}
```
