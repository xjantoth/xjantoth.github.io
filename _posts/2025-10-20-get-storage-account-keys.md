---
title: "Get Storage Account Keys"
date: "2022-01-06T14:15:29+0100"
lastmod: "2022-01-06T14:15:29+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to retrieve Azure Storage Account access keys using the Azure CLI."

tags: ['get', 'storage', 'account', 'keys']
categories: ["DevOps"]
---

Use the following Azure CLI command to list the access keys for a specific storage account. You need to provide the resource group name and the storage account name.

```bash
az storage account keys list --resource-group erste-dev-slack-rg --account-name erstedevstorage
```
