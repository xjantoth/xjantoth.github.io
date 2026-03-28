---
title: "Create ACM certificate"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to create and import SSL certificates into AWS ACM using EasyRSA for an AWS VPN endpoint setup."

tags: ['acm', 'certificate']
categories: ["DevOps"]
---

Reference: https://medium.com/@Ahmed_Ansar/how-to-setup-aws-vpn-endpoint-8b15e78fd8b0

Clone the EasyRSA repository, initialize the PKI, build the certificate authority, and generate server and client certificates. These are needed for mutual TLS authentication with the AWS VPN endpoint.

```bash
git clone https://github.com/OpenVPN/easy-rsa.git
cd easy-rsa/easyrsa3
./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa build-server-full server nopass
/easyrsa build-client-full client1.domain.tld nopass
```

Import the generated server and client certificates into AWS ACM. The `--certificate-chain` parameter specifies the CA certificate used to sign the server and client certificates.

```bash
aws acm import-certificate --certificate file://./pki/issued/server.crt --private-key file://./pki/private/server.key  --certificate-chain file://./pki/ca.crt --region eu-central-1

aws acm import-certificate --certificate file://./pki/issued/client1.domain.tld.crt --private-key file://./pki/private/client1.domain.tld.key  --certificate-chain file://./pki/ca.crt --region eu-central-1

```
