---
title: GCP PCA certification notes
date: 2024-04-24T11:15:06+0200
lastmod: 2024-04-24T11:15:06+0200
draft: false
description: "Notes from GCP Professional Cloud Architect certification preparation covering gcloud profiles, Cloud Functions, Cloud Run, and container image management."
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['bash', 'gcp', 'gcloud', 'devopsinuse']
categories: ["GCP"]
---

# Using multiple gcloud configurations/profile

You can maintain multiple gcloud configuration profiles to switch between different GCP accounts and projects. Each profile stores its own core settings such as the account, custom CA certificates, and authentication preferences. This is especially useful when working across several GCP organizations or behind a corporate proxy.

```bash
v ~/.config/gcloud/configurations/config_profile1
...
[core]
custom_ca_certs_file = /Users/AAAA/Documents/proxyCA.crt
account = user1@address.net

[auth]
disable_ssl_validation = True
...
:wq!


v ~/.config/gcloud/configurations/config_profile2
...
[core]
custom_ca_certs_file = /Users/AAAA/Documents/proxyCA.crt
account = user2@address.net

[auth]
disable_ssl_validation = True
...
:wq!


gcloud auth list
gcloud config configurations activate profile1
gcloud config configurations activate profile2
```


# Cloud Functions 2nd gen.

Cloud Functions 2nd generation is backed by Cloud Run under the hood. You can list, invoke, and inspect Cloud Functions using `gcloud functions` commands. To retrieve the function URL, use `jq` to parse the JSON output.

```bash
gcloud functions list
gcloud functions call function-2 --region europe-west3  --data='{"name": "Hello World!"}'
gcloud functions describe --format="json"  function-2 --region europe-west3 | jq -r '.serviceConfig.uri'
gcloud functions describe --format="json"  function-2 --region europe-west3 | jq -r '.url'

# since this function is 2nd gen -> backed by Cloud Run
gcloud run services list


```


# Cloud Run

Building container image via nerdctl/lima at macOS. The following Dockerfile creates a simple Nginx container that serves a static page, which can then be deployed to Cloud Run.

```dockerfile
Dockerfile

...
# Pull base image
FROM nginx

# Dockerfile Maintainer
MAINTAINER Jan Toth "helo@jan.com"


RUN echo "Hello PCA" > /usr/share/nginx/html/index.html

# Expose HTTP
EXPOSE 8080
...
:wq


nerdctl build -t europe-west3-docker.pkg.dev/vocal-park-416917/pca/nginx:v1 -f Dockerfile .

```

After building the image, authenticate to the Artifact Registry using an OAuth2 access token and push the image.

```bash
gcloud auth print-access-token k3scourse@gmail.com
nerdctl.lima login -u oauth2accesstoken  https://europe-west3-docker.pkg.dev

nerdctl.lima push europe-west3-docker.pkg.dev/vocal-park-416917/pca/nginx:v1

```

# List container images

```bash
gcloud artifacts docker images list europe-west3-docker.pkg.dev/vocal-park-416917/pca/

IMAGE                                                    DIGEST                                                                   CREATE_TIME          UPDATE_TIME
europe-west3-docker.pkg.dev/vocal-park-416917/pca/nginx  sha256:e16a4b9c7dde084c0c8657a19adeefee92cf71ab60db71f47eaf8145e49f8a76  2024-04-24T16:41:57  2024-04-24T16:41:57

```

# Deploy Cloud Run from local Dockerfile. There is no need to build container locally. Simply use the flag `--source .`

Cloud Run can build and deploy directly from source using `--source .`, which runs Cloud Build behind the scenes. The `--no-traffic` flag lets you deploy a new revision without routing traffic to it, enabling gradual rollouts.

```bash
# This command is equivalent to running `gcloud builds submit --tag [IMAGE] .` and `gcloud run deploy jans-cr --image [IMAGE]`


# Version5 (RUN echo "This is PCA Cloud run v5" >  /usr/share/nginx/html/index.html)
gcloud run deploy crun-source --source . --region=europe-west1 --allow-unauthenticated --port=80

# Version 6 (RUN echo "This is PCA Cloud run v6" >  /usr/share/nginx/html/index.html)
# This version is not being served yet
gcloud run deploy crun-source --source . --region=europe-west1 --allow-unauthenticated --port=80 --no-traffic


# Serve both revision 50:50
gcloud run revisions list --service crun-source --region europe-west1
   REVISION               ACTIVE  SERVICE      DEPLOYED                 DEPLOYED BY
✔  crun-source-00003-hvt  yes     crun-source  2024-04-24 19:03:07 UTC  aaaaaaaae@gmail.com
✔  crun-source-00002-nbm  yes     crun-source  2024-04-24 19:01:27 UTC  aaaaaaaae@gmail.com
✔  crun-source-00001-zhp          crun-source  2024-04-24 18:56:30 UTC  aaaaaaaae@gmail.com

gcloud run services update-traffic crun-source --to-revisions=crun-source-00003-hvt=50,crun-source-00002-nbm=50 --region=europe-west1

# Promote latest tested version
gcloud run services update-traffic crun-source --to-revisions=crun-source-00003-hvt=100 --region=europe-west1

curl https://crun-source-k3ep63kthq-ew.a.run.app
This is PCA Cloud run v6


# Delete Cloud Run service
gcloud run services delete cr --region=europe-west3
```




