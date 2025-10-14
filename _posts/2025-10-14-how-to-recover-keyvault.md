---
title: "How to recover keyvault"
date: 2022-02-09T11:04:38+0100
lastmod: 2022-02-09T11:04:38+0100
draft: false
description: "How to recover keyvault"
image: "images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - azure
  - keyvault
---

A simple way how to recover Azrue keyvault if needed

```
az group create --location westeurope --resource-group "erste-compliance-dev-rg"
az keyvault recover -n "erste-compliance-dev-kv" -g "erste-compliance-dev-rg"
az keyvault secret list-deleted --vault-name "erste-compliance-dev-kv" | grep name > /tmp/secrets
cat /tmp/secrets | while read secret; do az keyvault secret recover  --vault-name "erste-compliance-dev-kv" --name "$secret"; done

cat /tmp/secrets
  azureClientId
  azureClientSecret
  azureTenantId
  endpointSuffix
  storageAccountResourceTableName
```
