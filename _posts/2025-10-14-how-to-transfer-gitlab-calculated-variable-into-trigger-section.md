---
title: "How to transfer gitlab calculated variable into trigger section"
date: 2022-07-18T13:39:59+0200
lastmod: 2022-07-18T13:39:59+0200
draft: false
description: "One has to used artifacts section combined with reports child keyword and save a variable with its value to build.env file."
image: "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['gitlab', 'variables']
categories: ["CI/CD"]
---

One has to used `artifacts` section combined with `reports` child keyword and save a variable with its value to `build.env` file.
https://techhelpnotes.com/gitlab-ci-pass-variable-to-a-trigger-stage/


```yaml
create_profile:
  stage: build
  script:
  # calculate APPLICATION_VERSION
    - echo APPLICATION_VERSION=0.1.0 >> build.env
    - echo Create profile ${APPLICATION_NAME} with version ${APPLICATION_VERSION}
  artifacts:
    paths:
      - profile
    reports:
      dotenv: build.env

trigger_upload:
  stage: release
  variables:
    PROFILE_NAME: ${APPLICATION_NAME}
    PROFILE_VERSION: ${APPLICATION_VERSION}
  trigger:
    project: git-project/profile-uploader
    strategy: depend
  needs:
    - job: create_profile
      artifacts: true
```
