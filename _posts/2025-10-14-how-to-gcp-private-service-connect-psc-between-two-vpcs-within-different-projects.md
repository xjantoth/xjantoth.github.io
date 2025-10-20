---
title: How to GCP Private Service Connect PSC between two VPCs within different projects
date: 2024-05-17T20:08:32+0200
lastmod: 2024-05-17T20:08:32+0200
draft: false
description: How to GCP Private Service Connect PSC between two VPCs within different projects
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['bash', 'devopsinuse', 'gcp', 'psc']
---


![Image](/assets/images/blog/psc.drawio.png)
### Create 2 new GCP Projects in Free Tier Account


```
gcloud projects create consumer-cmd --name="consumer-cmd" --enable-cloud-apis
gcloud projects create producer-cmd --name="producer-cmd" --enable-cloud-apis

# verify creation
[arch:devopsinuse main()U] gcloud projects list

PROJECT_ID         NAME            PROJECT_NUMBER
...                ...             ...
consumer-cmd       consumer-cmd    493498333648
producer-cmd       producer-cmd    699309020362
```


### Check billing account

```
gcloud alpha billing accounts list --format json
[
  {
    "displayName": "My Billing Account",
    "masterBillingAccount": "",
    "name": "billingAccounts/013B47-F4F5F8-EC14F6",
    "open": true,
    "parent": ""
  }
]

```

### Startup script debugging

```
# The correct answer (by now) is to use journalctl:
sudo journalctl -u google-startup-scripts.service

# You can re-run a startup script like this:
sudo google_metadata_script_runner --script-type startup
```

### Manually enable compute API

I have not found an option to enable compute API other than via GCP Console web interface.

Later on

```
gcloud services enable networkservices.googleapis.com --project consumer-cmd
gcloud services enable networkservices.googleapis.com --project producer-cmd

gcloud auth application-default login
gcloud auth list
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/gcloud/application_default_credentials.json
```


### Terraform code

```
terraform {
  required_version = ">= 1.6.6"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.29.1"
    }
  }
}

locals {
  region           = "europe-west3"
  vm_size          = "n2-standard-2"
  user             = "user"
  consumer-proj-id = "493498333648"
  consumer_prefix  = "consumer-cmd"
  producer_prefix  = "producer-cmd"
}

provider "google" {
  # Configuration options
  # gcloud projects list
  # PROJECT_ID         NAME            PROJECT_NUMBER
  # consumer-cmd       consumer-cmd    493498333648
  # producer-cmd       producer-cmd    699309020362

}

# ssh-keygen -f assessment -t rsa -b 4096 -C "user@external.com"

resource "google_compute_network" "consumer" {
  project                 = local.consumer_prefix
  name                    = "vpc-${local.consumer_prefix}"
  auto_create_subnetworks = false
  mtu                     = 1460
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "consumer" {
  project       = local.consumer_prefix
  name          = "subnet-${local.consumer_prefix}-${local.region}"
  ip_cidr_range = "10.0.0.0/24"
  region        = local.region
  network       = google_compute_network.consumer.id
  #tfsec:ignore:google-compute-enable-vpc-flow-logs
  stack_type = "IPV4_ONLY"
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

resource "google_compute_firewall" "consumer" {
  project = local.consumer_prefix
  name    = "fw-${local.consumer_prefix}-${local.region}"
  network = google_compute_network.consumer.self_link
  #tfsec:ignore:google-compute-no-public-ingress
  source_ranges = ["0.0.0.0/0"]
  direction     = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}

resource "google_compute_instance" "consumer" {
  project      = local.consumer_prefix
  name         = local.consumer_prefix
  machine_type = local.vm_size
  zone         = "${local.region}-a"

  tags = [local.consumer_prefix, "vm", "gcp", "terraform", "consumer"]

  #tfsec:ignore:google-compute-vm-disk-encryption-customer-key
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        my_label = local.consumer_prefix
      }
    }
  }
  # when you want to change instance type
  allow_stopping_for_update = true

  network_interface {
    network    = google_compute_network.consumer.id
    subnetwork = google_compute_subnetwork.consumer.id

    #tfsec:ignore:google-compute-no-public-ip
    access_config {
      // Ephemeral public IP will be provided
    }
  }

  metadata = {
    block-project-ssh-keys = true
    ssh-keys               = "${local.user}:${file("assessment.pub")}"
  }

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }

}

output "ssh" {
  description = "SSH command copy/paste."
  value       = "ssh -i assessment ${local.user}@${google_compute_instance.consumer.network_interface[0].access_config[0].nat_ip}"
}


# .................................................................................
# Procucer section
# .................................................................................

resource "google_compute_network" "producer" {
  project                 = local.producer_prefix
  name                    = "vpc-${local.producer_prefix}"
  auto_create_subnetworks = false
  mtu                     = 1460
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "third-party-subnet" {
  project       = local.producer_prefix
  name          = "subnet-${local.producer_prefix}-${local.region}-third-party"
  ip_cidr_range = "10.0.0.0/24"
  region        = local.region
  network       = google_compute_network.producer.id
  #tfsec:ignore:google-compute-enable-vpc-flow-logs
  stack_type = "IPV4_ONLY"
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

resource "google_compute_subnetwork" "psc-subnet-producer" {
  project       = local.producer_prefix
  name          = "psc-subnet-${local.producer_prefix}-${local.region}"
  ip_cidr_range = "10.100.0.0/24"
  purpose       = "PRIVATE_SERVICE_CONNECT"
  region        = local.region
  network       = google_compute_network.producer.id
  #tfsec:ignore:google-compute-enable-vpc-flow-logs
  stack_type = "IPV4_ONLY"
  log_config {
    aggregation_interval = "INTERVAL_10_MIN"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

resource "google_compute_firewall" "producer" {
  project = local.producer_prefix
  name    = "fw-${local.producer_prefix}-${local.region}"
  network = google_compute_network.producer.self_link
  #tfsec:ignore:google-compute-no-public-ingress
  source_ranges = ["0.0.0.0/0"]
  direction     = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["22", "80"]
  }
}

resource "google_compute_instance_template" "apache" {
  project     = local.producer_prefix
  name        = "apache-template"
  description = "This template is used to create Apache Web Server (PSC test)."

  tags = ["psc", "provider", "terraform"]

  labels = {
    environment = "test"
  }

  instance_description = "Apache2 PSC test"
  machine_type         = "n2-standard-2"
  can_ip_forward       = false

  scheduling {
    automatic_restart   = true
    on_host_maintenance = "MIGRATE"
  }

  // Create a new boot disk from an image
  disk {
    source_image = "debian-cloud/debian-11"
    auto_delete  = true
    boot         = true
    // backup the disk every day
  }


  network_interface {
    network    = google_compute_network.producer.id
    subnetwork = google_compute_subnetwork.third-party-subnet.id

    #tfsec:ignore:google-compute-no-public-ip
    access_config {
      // Ephemeral public IP will be provided
    }
  }

  metadata = {
    block-project-ssh-keys = true
    ssh-keys               = "${local.user}:${file("assessment.pub")}"
    startup-script         = <<-EOF
    #!/bin/sh
    set -e
    apt-get update
    apt-get install apache2 -y
    echo "This is an artificial Third Party Service exposed via PSC from producer-cmd project over to consumer-cmd project" > /var/www/html/index.html
    systemctl restart apache2
    EOF
  }

}


resource "google_compute_instance_group_manager" "third-party-ig" {
  project = local.producer_prefix
  name    = "third-party-ig"

  base_instance_name = "apache"
  zone               = "${local.region}-a"

  version {
    instance_template = google_compute_instance_template.apache.self_link_unique
  }

  all_instances_config {
    metadata = {
    }
    labels = {
      usecase   = "psc"
      terraform = "true"
      vpc       = "producer"
    }
  }

  # target_pools = [google_compute_target_pool.appserver.id]
  target_size = 1

  named_port {
    name = "httpd"
    port = 80
  }

  auto_healing_policies {
    health_check      = google_compute_health_check.autohealing.id
    initial_delay_sec = 300
  }
}

resource "google_compute_health_check" "autohealing" {
  project             = local.producer_prefix
  name                = "autohealing-health-check"
  check_interval_sec  = 5
  timeout_sec         = 5
  healthy_threshold   = 2
  unhealthy_threshold = 10 # 50 seconds

  http_health_check {
    request_path = "/"
    port         = "80"
  }
}

# https://github.com/GoogleCloudPlatform/cloud-foundation-fabric/tree/master/modules/net-lb-int
# https://cloud.google.com/load-balancing/docs/internal/int-tcp-udp-lb-tf-module-examples
resource "google_compute_forwarding_rule" "google_compute_forwarding_rule" {
  project               = local.producer_prefix
  name                  = "l4-ilb-forwarding-rule"
  backend_service       = google_compute_region_backend_service.default.id
  region                = "europe-west3"
  ip_protocol           = "TCP"
  load_balancing_scheme = "INTERNAL"
  all_ports             = true
  allow_global_access   = true
  network               = google_compute_network.producer.id
  subnetwork            = google_compute_subnetwork.third-party-subnet.id
}

resource "google_compute_region_backend_service" "default" {
  project               = local.producer_prefix
  name                  = "l4-ilb-backend-subnet"
  region                = "europe-west3"
  protocol              = "TCP"
  load_balancing_scheme = "INTERNAL"
  health_checks         = [google_compute_health_check.autohealing.id]
  backend {
    group          = google_compute_instance_group_manager.third-party-ig.instance_group
    balancing_mode = "CONNECTION"
  }
}

# Private Service Connect - Procucer site
# !!! this resource will be created in "Private Service Connect" > "PUBLISHED SERVICES" as expected
# the keyword "attachment" is rather misleading for me in terraform resource name!
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_service_attachment
resource "google_compute_service_attachment" "psc_ilb_service_attachment" {
  project     = local.producer_prefix
  name        = local.producer_prefix
  region      = local.region
  description = "A service attachment configured with Terraform"

  # domain_names             = ["gcp.tfacc.hashicorptest.com."]
  enable_proxy_protocol = false
  connection_preference = "ACCEPT_MANUAL"
  nat_subnets           = [google_compute_subnetwork.psc-subnet-producer.id]
  target_service        = google_compute_forwarding_rule.google_compute_forwarding_rule.id

  consumer_accept_lists {
    project_id_or_num = local.consumer-proj-id
    connection_limit  = 10
  }
}

# Consumer Site "Private Service Connect" > "Connected Endpoints"
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_forwarding_rule#example-usage---forwarding-rule-vpc-psc
// Forwarding rule for VPC private service connect
resource "google_compute_forwarding_rule" "default" {
  project               = local.consumer_prefix
  name                  = "psc-endpoint-${local.consumer_prefix}"
  region                = local.region
  load_balancing_scheme = ""
  target                = google_compute_service_attachment.psc_ilb_service_attachment.id
  network               = google_compute_network.consumer.id
  ip_address            = google_compute_address.consumer_address.id
  # allow_psc_global_access: (Optional) This is used in PSC consumer ForwardingRule to control whether the PSC endpoint can be accessed from another region.
  allow_psc_global_access = false
}

// Consumer service endpoint
resource "google_compute_address" "consumer_address" {
  project      = local.consumer_prefix
  name         = "ipv4-consumer-endpoint"
  region       = local.region
  subnetwork   = google_compute_subnetwork.consumer.id
  address_type = "INTERNAL"
}

output "mig" {
  description = "mig"
  # value       = "ssh -i assessment ${local.user}@${google_compute_instance.third-party-subnet.network_interface[0].access_config[0].nat_ip}"
  value = google_compute_instance_group_manager.third-party-ig
}



```

### Apply terrafrom code

```
terraform apply
# Connect to consumer VM from wher we will test connection to producer project procuder vpc
ssh -i assessment user@34.159.3.56

```

>  Private Service Connect - Procucer site
> this resource will be created in "Private Service Connect" > "PUBLISHED SERVICES" as expected
the keyword "attachment" is rather misleading for me in terraform resource name!
https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_service_attachment


### Consumer section
![Image](/assets/images/blog/psc-1.png)
![Image](/assets/images/blog/psc-2.png)

### Producer section
![Image](/assets/images/blog/psc-3.png)
![Image](/assets/images/blog/psc-4.png)
![Image](/assets/images/blog/psc-5.png)
![Image](/assets/images/blog/psc-6.png)
![Image](/assets/images/blog/psc-7.png)




Video: https://www.youtube.com/watch?v=PUxvJJeSrIc



## Links:

202405172005
