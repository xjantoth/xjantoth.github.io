---
title: "How to compare sha512sum binaries for CKS"
date: 2025-12-29T17:31:29:+0100
lastmod: 2025-12-29T17:31:29:+0100
draft: false
description: "How to compare sha512sum binaries for CKS"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ["cks", "sha512sum", "vim", "sed"]
---

```bash
vim file.txt
...
kube-apiserver f417c0555bc0167355589dd1afe23be9bf909bf98312b1025f12015d1b58a1c62c9908c0067a7764fa35efdac7016a9efa8711a44425dd6692906a7c283f032c
kube-controller-manager 60100cc725e91fe1a949e1b2d0474237844b5862556e25c2c655a33boa8225855ec5ee22fa4927e6c46a60d43a7c4403a27268f96fbb726307d1608b44f38a60
kube-proxy 52f9d8ad045f8eee1d689619ef8ceef2d86d50c75a6a332653240d7ba5b2a114aca056d9e513984ade24358c9662714973c1960c62a5cb37dd375631c8a614c6
kubelet 4be40f2440619e990897cf956c32800dc96c2c983bf64519854a3309fa5aa21827991559f9c44595098e27e6f2ee4d64a3fdec6baba8a177881f20e3ec61e26c
...

:%s/\v^(\S+)\s+(\S+)/echo \1; diff <(sha512sum \/path\/to\/\1 | cut -d" " -f1) <(echo \2)/g
...

echo kube-apiserver; diff <(sha512sum /path/to/kube-apiserver | cut -d" " -f1) <(echo f417c0555bc0167355589dd1afe23be9bf909bf98312b1025f12015d1b58a1c62c9908c0067a7764fa35efdac7016a9efa8711a44425dd6692906a7c283f032c)
echo kube-controller-manager; diff <(sha512sum /path/to/kube-controller-manager | cut -d" " -f1) <(echo 60100cc725e91fe1a949e1b2d0474237844b5862556e25c2c655a33boa8225855ec5ee22fa4927e6c46a60d43a7c4403a27268f96fbb726307d1608b44f38a60)
echo kube-proxy; diff <(sha512sum /path/to/kube-proxy | cut -d" " -f1) <(echo 52f9d8ad045f8eee1d689619ef8ceef2d86d50c75a6a332653240d7ba5b2a114aca056d9e513984ade24358c9662714973c1960c62a5cb37dd375631c8a614c6)
echo kubelet; diff <(sha512sum /path/to/kubelet | cut -d" " -f1) <(echo 4be40f2440619e990897cf956c32800dc96c2c983bf64519854a3309fa5aa21827991559f9c44595098e27e6f2ee4d64a3fdec6baba8a177881f20e3ec61e26c)
...

:wq!

```
