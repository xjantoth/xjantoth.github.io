---
title: "AWS ENV Credentials"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
description: "How to set AWS credentials via environment variables for CLI and SDK authentication."

tags: ['aws', 'env', 'credentials']
categories: ["AWS"]
---

You can authenticate the AWS CLI and SDKs by exporting credentials as environment variables. This approach is useful for temporary sessions or CI/CD pipelines where you do not want to persist credentials in `~/.aws/credentials`. Replace the placeholder values with your actual access key and secret key.

```bash
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="eu-central-1"
```
