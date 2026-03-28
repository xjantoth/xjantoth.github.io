---
title: "Jobs and CronJobs"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Jobs and CronJobs — practical walkthrough with examples."

tags: ['jobs', 'cronjobs']
categories: ["DevOps"]
---

##  Job

The following example creates a Kubernetes Job using `kubectl` with a dry-run to generate the YAML manifest, then customizes it with parallelism and completions settings.

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

A CronJob runs a Job on a recurring schedule defined with standard cron syntax. This example creates a CronJob that runs daily at 21:30.

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
