---
title: "How to aws cli with SSO"
date: "2022-01-04T13:36:26+0100"
lastmod: "2022-01-04T13:36:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/aws-1.jpg"
description: "How to aws cli with SSO"

tags: ['how', 'to', 'aws', 'cli', 'with', 'sso']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```
(venv) [arch:Downloads ] aws configure sso
SSO start URL [None]: https://devopsinuse.awsapps.com
SSO Region [None]: eu-central-1

An error occurred (InvalidRequestException) when calling the StartDeviceAuthorization operation:
(venv) [arch:Downloads ] aws configure sso
SSO start URL [None]: https://devopsinuse.awsapps.com/start/#/
SSO Region [None]: eu-central-1
Attempting to automatically open the SSO authorization page in your default browser.
If the browser does not open or you wish to use a different device to authorize this request, open the following URL:

https://device.sso.eu-central-1.amazonaws.com/

Then enter the code:

AAAF-XXXS
The only AWS account available to you is: 099021696655
Using the account ID 099021696655
The only role available to you is: AdministratorAccess
Using the role name "AdministratorAccess"
CLI default client Region [None]: eu-central-1
CLI default output format [None]:
CLI profile name [AdministratorAccess-099021696655]: devopsinuse

To use this profile, specify the profile name using --profile, as shown:

aws s3 ls --profile devopsinuse
(venv) [arch:Downloads ] aws s3 ls --profile devopsinuse
```

```
 cat  ~/.aws/config
[profile devopsinuse]
sso_start_url = https://devopsinuse.awsapps.com/start/#/
sso_region = eu-central-1
sso_account_id = 091111111155
sso_role_name = AdministratorAccess
region = eu-central-1
```
