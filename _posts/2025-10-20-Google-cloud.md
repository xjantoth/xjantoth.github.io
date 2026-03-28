---
title: "Google cloud"
date: "2022-01-06T15:00:26+0100"
lastmod: "2022-01-06T15:00:26+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
description: "Working with Google Cloud Platform using gcloud CLI, Terraform, Cloud Run, Memorystore Redis, and VPC connectors."

tags: ['google', 'cloud']
categories: ["GCP"]
---

**Terraform in my wadzpay-dev**

Set the service account credentials and configure the gcloud CLI to use the correct account and project for the wadzpay-dev environment.

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/jantoth/.google-cloud-keys/wadzpay-dev-cdb0bf1613d2.json
gcloud auth list
gcloud config set account jan.toth@vacuumlabs.com
gcloud config set project wadzpay-dev
```


**Terraform in my own account**

https://medium.com/swlh/how-to-deploy-a-cloud-sql-db-with-a-private-ip-only-using-terraform-e184b08eca64

Configure credentials for a personal GCP account, enable required APIs for Terraform, and run the Terraform workflow. The APIs include Compute, IAM, OS Login, Service Networking, and Cloud SQL Admin.

```bash
GOOGLE_APPLICATION_CREDENTIALS=/home/jantoth/.google-cloud-keys/consummate-atom-309219-0b338646619a.json

gcloud config set account kubernetes.certification@gmail.com
gcloud config set project consummate-atom-309219

# optional?
gcloud services enable \
    cloudresourcemanager.googleapis.com \
    compute.googleapis.com \
    iam.googleapis.com \
    oslogin.googleapis.com \
    servicenetworking.googleapis.com \
    sqladmin.googleapis.com

cd /home/jantoth/Documents/work/wadzpay-service/terraform-test
terraform init
terraform plan

```

**Notes:**

List and describe Redis instances in a specific GCP region.

```bash
gcloud config set account kubernetes.certification@gmail.com
gcloud config set project consummate-atom-309219


gcloud redis instances list --region europe-west3
gcloud redis instances describe  wadzpay-dev-tf --region europe-west3
```


**Article:''
https://medium.com/google-cloud/using-memorystore-with-cloud-run-82e3d61df016

```
# Clone a simple node js app
git clone https://github.com/kolban-google/accessing-memorystore-from-cloud-run.git
cd accessing-memorystore-from-cloud-run

# Build docker image
docker build -t gcr.io/consummate-atom-309219/cloud-run-app .
docker push  gcr.io/consummate-atom-309219/cloud-run-app


# List redis instances in region
gcloud redis instances list --region europe-west3

# Describe already provisioned
 gcloud redis instances create redis1 --region  europe-west
gcloud redis instances describe redis1  --region europe-west3

# Create VPC connector
gcloud compute networks vpc-access connectors create my-vpc-connector --network default --region europe-west3  --range 10.8.0.0/28


gcloud run deploy cloud-run-app \
  --image gcr.io/consummate-atom-309219/cloud-run-app \
  --max-instances 1 \
  --platform managed \
  --region europe-west3 \
  --vpc-connector my-vpc-connector \
  --allow-unauthenticated \
  --set-env-vars "REDIS_IP=10.148.60.211,PSQL_HOST=10.124.32.3"
```
