---
title: "create ACM certificate"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/aws-1.jpg"
description: "create ACM certificate"

tags: ['create', 'acm', 'certificate']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

https://medium.com/@Ahmed_Ansar/how-to-setup-aws-vpn-endpoint-8b15e78fd8b0

```
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
/easyrsa build-client-full client1.domain.tld nopass
```


```
aws acm import-certificate --certificate file://./pki/issued/server.crt --private-key file://./pki/private/server.key  --certificate-chain file://./pki/ca.crt --region eu-central-1

aws acm import-certificate --certificate file://./pki/issued/client1.domain.tld.crt --private-key file://./pki/private/client1.domain.tld.key  --certificate-chain file://./pki/ca.crt --region eu-central-1

```
