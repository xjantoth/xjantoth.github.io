---
title: How to create a clonable proxmox Ubuntu VM
date: 2024-10-04T14:41:24+0100
lastmod: 2024-10-04T14:41:24+0100
draft: false
description: How to create a clonable proxmox Ubuntu VM
image: "https://www.codeschoepfer.de/wp-content/uploads/2024/05/proxmox-blog-960_480.jpg"
author: "Jan Toth"
tags: ['bash', 'proxmox', 'kvm', 'clone', 'devopsinuse']
---

Referece: https://github.com/caiocampoos/homelab-k8s/blob/main/vm-templates/ubuntu-22.04/ubuntu-22.04.sh

ISO: https://old-releases.ubuntu.com/releases/24.04/SHA256SUMS

Cloud images: http://cloud-images.ubuntu.com/releases/jammy/release/

# Configure and create Proxmox template with Packer

```
vim template-creds.pkr.hcl

...
proxmox_api_url = "https://192.168.0.224:8006/api2/json"
proxmox_api_token_id = "root@pam!Packer"
proxmox_api_token_secret = "ea0a6743-126c-48b2-a704-a223b36017a4"
...



```

```bash
#!/bin/sh

### variables
VM_TEMPLATE_ID=999
TEMPLATE_NAME='ubuntu-2204-template'
UBUNTU_IMAGE='ubuntu-22.04-server-cloudimg-amd64-disk-kvm.img'
UBUNTU_IMAGE_QCOW2='ubuntu-22.04.qcow2'
USERNAME='ubuntu'
PASSWORD='...'
MEMORY='4096'
CPUS='2'
### variables


# install tools
apt update -y && apt install nano wget curl libguestfs-tools -y

# remove old image
rm -rfv ${UBUNTU_IMAGE}

# remove old template container - WILL DESTROY COMPLETELY
qm destroy ${VM_TEMPLATE_ID} --destroy-unreferenced-disks 1 --purge 1

# download new image
wget http://cloud-images.ubuntu.com/releases/22.04/release/${UBUNTU_IMAGE}

# add agent to image
virt-customize -a ${UBUNTU_IMAGE} --install qemu-guest-agent

# change extension to qcow2
mv ${UBUNTU_IMAGE} ${UBUNTU_IMAGE_QCOW2}

# increase image
qemu-img resize ${UBUNTU_IMAGE_QCOW2} +30G

# create the vm
qm create ${VM_TEMPLATE_ID} --memory ${MEMORY} --cores ${CPUS} --net0 virtio,bridge=vmbr0 --name ${TEMPLATE_NAME} --scsihw virtio-scsi-pci

# configure the vm  
qm set ${VM_TEMPLATE_ID} --scsi0 local-lvm:0,import-from=/root/${UBUNTU_IMAGE_QCOW2}
qm set ${VM_TEMPLATE_ID} --ide2 local-lvm:cloudinit
qm set ${VM_TEMPLATE_ID} --boot order=scsi0
qm set ${VM_TEMPLATE_ID} --serial0 socket --vga serial0
qm set ${VM_TEMPLATE_ID} --ipconfig0 ip=dhcp
qm set ${VM_TEMPLATE_ID} --agent enabled=1
qm set ${VM_TEMPLATE_ID} -ciuser ${USERNAME}
qm set ${VM_TEMPLATE_ID} -cipassword ${PASSWORD}
qm set ${VM_TEMPLATE_ID} --sshkeys ~/.ssh/authorized_keys

# convert to template
qm template ${VM_TEMPLATE_ID} 

# remove new template
rm -rfv ${UBUNTU_IMAGE_QCOW2}
```
