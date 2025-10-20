---
title: "Protect Kubernetes node metadata"
date: 2022-02-21T13:54:39+0100
lastmod: 2022-02-21T13:54:39+0100
draft: false
description: "Protect Kubernetes node metadata"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['protect', 'kubernetes', 'node', 'metadata']
---

###### Deny all traffic to google's metadata server

Study this rule carefully - it takes time to understand it :)

```yaml
cat <<'EOF' > np_cloud_metadata_deny.yaml
# all pods in namespace cannot access metadata endpoint
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-metadata-deny
  namespace: default
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 0.0.0.0/0            # < --- thanks to this rule PODS have an access everywhere, but 169.254.169.254!!!
        except:
        - 169.254.169.254/32
EOF
```

###### Allow certain pods to access this server


```yaml

cat <<'EOF' > np_cloud_metadata_allow.yaml
# only pods with label are allowed to access metadata endpoint
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: cloud-metadata-allow
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: metadata-accessor       # < --- thanks to this rule PODS with metadata-accessor would additionally have an access to 169.254.169.254 too !!!
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 169.254.169.254/32
EOF
```
