---
title: "Notebook serial number"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "Notebook serial number"

tags: ['notebook', 'serial', 'number']
image: "/assets/images/blog/linux-1.jpg"
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```bahs
Ak by ste chceli vediet model a seriove cislo svojho notebooku:
 Serial Number: PF24KS2B
$ sudo dmidecode | grep -i serial
        Serial Number: 00000000
        Serial Number: 2C153768
        Serial Number: None
                Serial services are supported (int 14h)
        Serial Number: PF24KS2B
        Serial Number: L1HF0B201Z7
        Serial Number: PF24KS2B
        SBDS Serial Number: 0A4A
Model: ThinkPad T15 Gen 1
$ sudo dmidecode | grep -i sku
                Consumer SKU
        SKU Number: LENOVO_MT_20S6_BU_Think_FM_ThinkPad T15 Gen 1
        SKU Number: Not Specified
```
