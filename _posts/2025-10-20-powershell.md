---
title: "PowerShell"
date: "2022-01-06T14:15:29+0100"
lastmod: "2022-01-06T14:15:29+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Connect to Azure via PowerShell using the Connect-AzAccount cmdlet."

tags: ['powershell']
categories: ["DevOps"]
---

Connect to Azure via PowerShell

The `Connect-AzAccount` cmdlet opens an interactive login prompt to authenticate your PowerShell session with Azure. Once authenticated, you can use the Az module cmdlets to manage Azure resources.

```powershell
# Connect to Azure via PowerShell
Connect-AzAccount
```
