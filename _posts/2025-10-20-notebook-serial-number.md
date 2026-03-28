---
title: "Notebook serial number"
date: "2022-01-04T12:47:26+0100"
lastmod: "2022-01-04T12:47:26+0100"
draft: false
author: "Jan Toth"
description: "How to retrieve the serial number and model of your Linux notebook using dmidecode."

tags: ['notebook', 'serial', 'number']
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
categories: ["DevOps"]
---

If you want to find the model and serial number of your notebook, you can use the `dmidecode` command. This reads hardware information from the system's DMI/SMBIOS tables. The example below shows how to filter for serial number and SKU information.

```bash
# Serial Number: PF24KS2B
sudo dmidecode | grep -i serial
        Serial Number: 00000000
        Serial Number: 2C153768
        Serial Number: None
                Serial services are supported (int 14h)
        Serial Number: PF24KS2B
        Serial Number: L1HF0B201Z7
        Serial Number: PF24KS2B
        SBDS Serial Number: 0A4A
Model: ThinkPad T15 Gen 1

sudo dmidecode | grep -i sku
                Consumer SKU
        SKU Number: LENOVO_MT_20S6_BU_Think_FM_ThinkPad T15 Gen 1
        SKU Number: Not Specified
```
