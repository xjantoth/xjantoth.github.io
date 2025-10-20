---
title: "Jobs and CronJobs"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Jobs and CronJobs"

tags: ['jobs', 'and', 'cronjobs']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

##  Job

```yaml
# Create job skeleton
kubectl  create job throw-dice-job --image=kodekloud/throw-dice --dry-run=client -o yaml > job.yaml

# Add few detail to a definition file
cat job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  creationTimestamp: null
  name: throw-dice-job
spec:
  parallelism: 3
  completions: 3
  template:
    metadata:
      creationTimestamp: null
    spec:
      containers:
      - image: kodekloud/throw-dice
        name: throw-dice-job
        resources: {}
      restartPolicy: Never
status: {}
```

##  CronJob

```yaml
kubectl  create cronjob throw-dice-cron-job --image=kodekloud/throw-dice --schedule="30 21 * * *"
cronjob.batch/throw-dice-cron-job created
controlplane $

cat cron.yaml
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  creationTimestamp: null
  name: throw-dice-cron-job
spec:
  jobTemplate:
    metadata:
      creationTimestamp: null
      name: throw-dice-cron-job
    spec:
      template:
        metadata:
          creationTimestamp: null
        spec:
          containers:
          - image: kodekloud/throw-dice
            name: throw-dice-cron-job
            resources: {}
          restartPolicy: OnFailure
  schedule: 30 21 * * *
status: {}
```
