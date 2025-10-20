---
title: "Google cloud pipeline example"
date: "2022-01-06T15:00:26+0100"
lastmod: "2022-01-06T15:00:26+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/gcp-1.jpg"
description: "Google cloud pipeline example"

tags: ['google', 'cloud', 'pipeline', 'example']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

**cloudbuild.yaml''

```yaml
steps:
- id: 'Get wadzpay docker image tag from build.gradle.kts'
  name: ubuntu
  entrypoint: bash
  args:
    - -c
    - |
      # Getting docker image TAG and passing it through further build steps
      echo "$(cat build.gradle.kts| grep -e "^version" | cut -d= -f2 | tr -d "\" ")" > /workspace/docker_image_tag.txt

- id: 'Build docker image'
  name: 'gcr.io/cloud-builders/docker'
  entrypoint: 'bash'
  args: ['-c', 'docker build -t ${_IMAGE}:$(cat /workspace/docker_image_tag.txt) .']

- id: 'Push docker image to Google Container Registry'
  name: 'gcr.io/cloud-builders/docker'
  entrypoint: 'bash'
  args: ['-c', 'docker push ${_IMAGE}:$(cat /workspace/docker_image_tag.txt)']

# Deploy container image to Cloud Run
- id: 'Deploy a new docker version to Cloud Run'
  name: 'gcr.io/cloud-builders/gcloud'
  entrypoint: 'bash'
  args: [
            '-c',
            'gcloud run deploy ${_CLOUD_RUN_SVC_NAME} --image ${_IMAGE}:$(cat /workspace/docker_image_tag.txt) --region ${_REGION} --platform managed --allow-unauthenticated'
        ]

substitutions:
  _IMAGE: "gcr.io/wadzpay-dev/wadzpay-service"
  _CLOUD_RUN_SVC_NAME: 'wadzpay-dev-tf'
  _REGION: 'europe-west3'

#images:
#- gcr.io/wadzpay-dev/wadzpay-service:${_TAG}
```
