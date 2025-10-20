---
title: "CKS testing mock"
date: 2022-08-29T11:08:34+0200
lastmod: 2022-08-29T11:08:34+0200
draft: false
description: "CKS testing mock"
image: "/assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags: ['cks', 'testing', 'mock']
---

##### kube-apiserver manifest with PodSecurityPolicy, ImagePolicyWebhook, Auditing
```
cat /etc/kubernetes/manifests/kube-apiserver.yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.16.247.9:6443
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=10.16.247.9
    - --allow-privileged=true
    - --authorization-mode=Node,RBAC
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --enable-admission-plugins=NodeRestriction,PodSecurityPolicy,ImagePolicyWebhook
    - --enable-bootstrap-token-auth=true
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
    - --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
    - --etcd-servers=https://127.0.0.1:2379
    - --insecure-port=0
    - --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
    - --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
    - --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
    - --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
    - --requestheader-allowed-names=front-proxy-client
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --requestheader-extra-headers-prefix=X-Remote-Extra-
    - --requestheader-group-headers=X-Remote-Group
    - --requestheader-username-headers=X-Remote-User
    - --secure-port=6443
    - --service-account-issuer=https://kubernetes.default.svc.cluster.local
    - --service-account-key-file=/etc/kubernetes/pki/sa.pub
    - --service-account-signing-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=10.96.0.0/12
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
    -  --audit-policy-file=/etc/kubernetes/prod-audit.yaml
    -  --audit-log-path=/var/log/prod-secrets.log
    -  --audit-log-maxbackup=30
    -  --admission-control-config-file=/etc/kubernetes/pki/admission_configuration.yaml
    image: k8s.gcr.io/kube-apiserver:v1.20.0
    imagePullPolicy: IfNotPresent
    livenessProbe:
      failureThreshold: 8
      httpGet:
        host: 10.16.247.9
        path: /livez
        port: 6443
        scheme: HTTPS
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    name: kube-apiserver
    readinessProbe:
      failureThreshold: 3
      httpGet:
        host: 10.16.247.9
        path: /readyz
        port: 6443
        scheme: HTTPS
      periodSeconds: 1
      timeoutSeconds: 15
    resources:
      requests:
        cpu: 250m
    startupProbe:
      failureThreshold: 24
      httpGet:
        host: 10.16.247.9
        path: /livez
        port: 6443
        scheme: HTTPS
      initialDelaySeconds: 10
      periodSeconds: 10
      timeoutSeconds: 15
    volumeMounts:
    - mountPath: /etc/ssl/certs
      name: ca-certs
      readOnly: true
    - mountPath: /etc/ca-certificates
      name: etc-ca-certificates
      readOnly: true
    - mountPath: /etc/kubernetes/pki
      name: k8s-certs
      readOnly: true
    - mountPath: /usr/local/share/ca-certificates
      name: usr-local-share-ca-certificates
      readOnly: true
    - mountPath: /usr/share/ca-certificates
      name: usr-share-ca-certificates
      readOnly: true
    - mountPath: /etc/kubernetes/prod-audit.yaml
      name: audit
      readOnly: true
    - mountPath: /var/log/prod-secrets.log
      name: audit-log
      readOnly: false
  hostNetwork: true
  priorityClassName: system-node-critical
  volumes:
  - hostPath:
      path: /etc/ssl/certs
      type: DirectoryOrCreate
    name: ca-certs
  - hostPath:
      path: /etc/ca-certificates
      type: DirectoryOrCreate
    name: etc-ca-certificates
  - hostPath:
      path: /etc/kubernetes/pki
      type: DirectoryOrCreate
    name: k8s-certs
  - hostPath:
      path: /usr/local/share/ca-certificates
      type: DirectoryOrCreate
    name: usr-local-share-ca-certificates
  - hostPath:
      path: /usr/share/ca-certificates
      type: DirectoryOrCreate
    name: usr-share-ca-certificates
  - name: audit
    hostPath:
      path: /etc/kubernetes/prod-audit.yaml
      type: File

  - name: audit-log
    hostPath:
      path: /var/log/prod-secrets.log
      type: File
status: {}
```


##### Example of PodSecurityPolicy


```
cat 3.yaml
---
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: pod-psp
spec:
  privileged: false  # Jangan izinkan Pod-Pod yang _privileged_!
  # Sisanya isi kolom-kolom yang dibutuhkan
  seLinux:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  runAsUser:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  volumes:
  - 'configMap'
  - 'configMap'
  - 'secret'
  - 'emptyDir'
  - 'hostPath'
```

#### History

```
vim /var/lib/kubelet/config.yaml
systemctl daemon-reload
systemctl restart kubelet
k get pods
/root/publish_kubebench.sh
cp /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/kubea-piserver.yaml.orig
vim /etc/kubernetes/manifests/kube-apiserver.yaml
journalctl -f -u kubelet
kubesec scan  /root/kubesec-pod.yaml
kubesec scan  /root/kubesec-pod.yaml > /root/kubesec_success_report.json
k create role dev-write -n dev --verb=get,watch,list --resource=pods -o yaml --dry-run=client
k create role dev-write -n dev --verb=get,watch,list --resource=pods
k create sa developer -n dev
k create rolebinding dev-write-binding -n dev --role dev-write --serviceaccount=dev:developer -oyaml --dry-run=client
k create rolebinding dev-write-binding -n dev --role dev-write --serviceaccount=dev:developer
vim /root/dev-pod.yaml
k edit cm -n opa untrusted-registry
k create  -f /root/beta-pod.yaml
vim /etc/kubernetes/pki/admission_configuration.yaml
k get pods -n alpha
k get pods -n alpha solaris -o yaml
k edit  pods -n alpha solaris
k edit  pods -n alpha sonata
k delete  pods -n alpha sonata
k edit  pods -n alpha triton
k delete  pods -n alpha triton
```

##### Enable ImagePolicyWebhook

Important line in `kube-apiserver` manifest


```
- --enable-admission-plugins=NodeRestriction,PodSecurityPolicy,ImagePolicyWebhook
```


```
# AdmissionConfiguration
cat /etc/kubernetes/pki/admission_configuration.yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: ImagePolicyWebhook
  configuration:
    imagePolicy:
      kubeConfigFile: /etc/kubernetes/pki/admission_kube_config.yaml
      allowTTL: 50
      denyTTL: 50
      retryBackoff: 500
      defaultAllow: false

# kubeConfigFile
cat /etc/kubernetes/pki/admission_kube_config.yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/pki/server.crt
    server: https://image-bouncer-webhook:30080/image_policy
  name: bouncer_webhook
contexts:
- context:
    cluster: bouncer_webhook
    user: api-server
  name: bouncer_validator
current-context: bouncer_validator
preferences: {}
users:
- name: api-server
  user:
    client-certificate: /etc/kubernetes/pki/apiserver.crt
    client-key:  /etc/kubernetes/pki/apiserver.key
```

##### Mock 1 (Ques 1)

A pod has been created in the omni namespace. However, there are a couple of issues with it.

The pod has been created with more permissions than it needs.
It allows read access in the directory /usr/share/nginx/html/internal causing an Internal Site to be accessed publicly.

To check this, click on the button called Site (above the terminal) and add /internal/ to the end of the URL.
Use the below recommendations to fix this.
Use the AppArmor profile created at /etc/apparmor.d/frontend to restrict the internal site.
There are several service accounts created in the omni namespace. Apply the principle of least privilege and use the service account with the minimum privileges (excluding the default service account).
Once the pod is recreated with the correct service account, delete the other unused service accounts in omni namespace (excluding the default service account).

You can recreate the pod but do not create a new service accounts and do not use the default service account.
correct service account used?

obsolete service accounts deleted?

internal-site restricted?

pod running?

```
cat 1.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: nginx
  name: frontend-site
  namespace: omni
  annotations:
    # Tell Kubernetes to apply the AppArmor profile "k8s-apparmor-example-deny-write".
    # Note that this is ignored if the Kubernetes node is not running version 1.4 or greater.
    container.apparmor.security.beta.kubernetes.io/nginx: localhost/restricted-frontend
spec:
  containers:
  - image: nginx:alpine
    imagePullPolicy: IfNotPresent
    name: nginx
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /usr/share/nginx/html
      name: test-volume
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: controlplane
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: frontend-default
  serviceAccountName: frontend-default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - hostPath:
      path: /data/pages
      type: Directory
    name: test-volume
```

#### Mock 1 (Ques 2)

A pod has been created in the orion namespace. It uses secrets as environment variables. Extract the decoded secret for the CONNECTOR_PASSWORD and place it under /root/CKS/secrets/CONNECTOR_PASSWORD.
You are not done, instead of using secrets as an environment variable, mount the secret as a read-only volume at path /mnt/connector/password that can be then used by the application inside.

pod secured?
secret mounted as read-only?
existing secret extracted to file?

```
 cat 2.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: app-xyz
  name: app-xyz
  namespace: orion
spec:
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: app-xyz
    ports:
    - containerPort: 3306
      protocol: TCP
    resources: {}
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: default-token-w9spp
      readOnly: true
    - mountPath: /mnt/connector/password
      name: a-safe-secret
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: controlplane
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}
  serviceAccount: default
  serviceAccountName: default
  terminationGracePeriodSeconds: 30
  tolerations:
  - effect: NoExecute
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300
  - effect: NoExecute
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:
  - name: default-token-w9spp
    secret:
      defaultMode: 420
      secretName: default-token-w9spp
  - name: a-safe-secret
    secret:
      defaultMode: 420
      secretName: a-safe-secret
```

#### Mock 1 (Ques 3)

A number of pods have been created in the delta namespace. Using the trivy tool, which has been installed on the controlplane, identify and delete pods except the ones with least number of CRITICAL level vulnerabilities.

Note: Do not modify the objects in anyway other than deleting the ones that have critical vulnerabilities.

vulnerable pods deleted?
non-vulnerable pods running?


```
   53  k get pods -n delta -ojsonpath='{range .items[*]}{.metadata.name}{": trivy --severity=CRITICAL i "}{.spec.containers[*].image}{"\n"}{end}'
   54  k get pods -n delta -ojsonpath='{range .items[*]}{"trivy --severity=CRITICAL i "}{.spec.containers[*].image}{" | grep -i Total"}{"\n"}{end}'
   55  trivy --severity=CRITICAL i kodekloud/webapp-delayed-start | grep -i Total
   56  trivy --severity=CRITICAL i httpd:2-alpine | grep -i Total
   57  trivy --severity=CRITICAL i nginx:1.16 | grep -i Total
   58  trivy --severity=CRITICAL i httpd:2.4.33 | grep -i Total
   59  k delete pod -n delta simple-webapp-1 simple-webapp-3 simple-webapp-4
   60  k get pods -n delta
```

#### Mock 1 (Ques 4)

Create a new pod called audit-nginx in the default namespace using the nginx image. Secure the syscalls that this pod can use by using the audit.json seccomp profile in the pod's security context.
The audit.json is provided at /root/CKS directory. Make sure to move it under the profiles directory inside the default seccomp directory before creating the pod

audit-nginx uses the right image?
pod running?
pod uses the correct seccomp profile?

```
cat 4.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: audit-nginx
  name: audit-nginx
spec:
  securityContext:
    seccompProfile:
      type: Localhost
      localhostProfile: profiles/audit.json
  containers:
  - image: nginx
    name: audit-nginx
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```
#### Mock 2 (Ques 1)

A pod called redis-backend has been created in the prod-x12cs namespace. It has been exposed as a service of type ClusterIP. Using a network policy called allow-redis-access, lock down access to this pod only to the following:
1. Any pod in the same namespace with the label backend=prod-x12cs.
2. All pods in the prod-yx13cs namespace.
All other incoming connections should be blocked.

Use the existing labels when creating the network policy.
Network Policy applied on the correct pods?
Incoming traffic allowed from pods in prod-yx13cs namespace?
Incoming traffic allowed from pods with label backend=prod-x12cs ?

```
cat 1.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-redis-access
  namespace: prod-x12cs
spec:
  podSelector:
    matchLabels:
      run: redis-backend
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              access: redis
        - podSelector:
            matchLabels:
              backend: prod-x12cs
      ports:
        - protocol: TCP
          port: 6379
```

#### Mock 2 (Ques 2)

A few pods have been deployed in the apps-xyz namespace. There is a pod called redis-backend which serves as the backend for the apps app1 and app2. The pod called app3 on the other hand, does not need access to this redis-backend pod. Create a network policy called allow-app1-app2 that will only allow incoming traffic from app1 and app2 to the redis-pod.

Make sure that all the available labels are used correctly to target the correct pods. Do not make any other changes to these objects.

Network Policy created on correct pods?
app1 ingress allowed?
app2 ingress allowed?
app3 ingress not allowed?

```
cat 2.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-app1-app2
  namespace: apps-xyz
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              name: app1
        - podSelector:
            matchLabels:
              name: app2
      ports:
        - protocol: TCP
          port: 6379

root@controlplane:/# k get pods -n apps-xyz -o wide
NAME            READY   STATUS    RESTARTS   AGE   IP          NODE           NOMINATED NODE   READINESS GATES
app1            1/1     Running   0          12m   10.50.0.7   controlplane   <none>           <none>
app2            1/1     Running   0          12m   10.50.0.6   controlplane   <none>           <none>
app3            1/1     Running   0          12m   10.50.0.8   controlplane   <none>           <none>
redis-backend   1/1     Running   0          12m   10.50.0.5   controlplane   <none>           <none>

17  k get pods -n apps-xyz -o wide
18  k exec -it -n apps-xyz app1 -- nc -v -z 10.50.0.5:6379
19  k exec -it -n apps-xyz app2 -- nc -v -z 10.50.0.5:6379
20  k exec -it -n apps-xyz app3 -- nc -v -z 10.50.0.5:6379
```

#### Mock 2 (Ques 3)

A pod has been created in the gamma namespace using a service account called cluster-view. This service account has been granted additional permissions as compared to the default service account and can view resources cluster-wide on this Kubernetes cluster. While these permissions are important for the application in this pod to work, the secret token is still mounted on this pod.

Secure the pod in such a way that the secret token is no longer mounted on this pod. You may delete and recreate the pod.
Pod created with cluster-view service account?
secret token not mounted in the pod?

```
cat 3.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: apps-cluster-dash
  name: apps-cluster-dash
  namespace: gamma

spec:
  automountServiceAccountToken: false
  containers:
  - image: nginx
    imagePullPolicy: Always
    name: apps-cluster-dash
  serviceAccount: cluster-view
```

#### Mock 2 (Ques 4)

A pod in the sahara namespace has generated alerts that a shell was opened inside the container.
Change the format of the output so that it looks like below:
ALERT timestamp of the event without nanoseconds,User ID,the container id,the container image repository
Make sure to update the rule in such a way that the changes will persists across Falco updates.
You can refer the falco documentation Here

```
journalctl -f -u falco | grep -i sahara
vim "+:set hlsearch" "+/A shell was spawned in a container with an attached terminal" /etc/falco/falco_rules.yaml
```

```
<cat  /etc/falco/falco_rules.local.yaml
#
# Or override/append to any rule, macro, or list from the Default Rules
- rule: Terminal shell in container
  desc: A shell was used as the entrypoint/exec point into a container with an attached terminal.
  condition: >
    spawned_process and container
    and shell_procs and proc.tty != 0
    and container_entrypoint
    and not user_expected_terminal_shell_in_container_conditions
  output: >
   %evt.time.s %user.uid %container.id %container.image.repository
  priority: ALERT
  tags: [container, shell, mitre_execution]
```



#### Mock 2 (Ques 5)

martin is a developer who needs access to work on the dev-a, dev-b and dev-z namespace. He should have the ability to carry out any operation on any pod in dev-a and dev-b namespaces. However, on the dev-z namespace, he should only have the permission to get and list the pods.

The current set-up is too permissive and violates the above condition. Use the above requirement and secure martin's access in the cluster. You may re-create objects, however, make sure to use the same name as the ones in effect currently.

martin has unrestricted access to all pods in dev-a ?
martin has unrestricted access to all pods in dev-b ?
martin can only list and get pods in dev-z ?

```
 k describe role dev-user-access -n dev-z
Name:         dev-user-access
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  pods       []                 []              [*]
root@controlplane:/# k describe role dev-user-access -n dev-a
Name:         dev-user-access
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  pods       []                 []              [*]
root@controlplane:/# k describe role dev-user-access -n dev-b
Name:         dev-user-access
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  pods       []                 []              [*]


```

Edit role in `dev-z` namespace to be able to `get` and `list` only


```
k get role -n dev-z dev-user-access -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2022-08-29T11:50:35Z"
  managedFields:
  - apiVersion: rbac.authorization.k8s.io/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:rules: {}
    manager: kubectl-edit
    operation: Update
    time: "2022-08-29T12:20:55Z"
  name: dev-user-access
  namespace: dev-z
  resourceVersion: "9432"
  uid: e049cd7a-ed47-4230-9ca5-e087cab40087
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - get
  - list
```

Test:


```
root@controlplane:/# k auth can-i --as martin create pod -n dev-a
yes
root@controlplane:/# k auth can-i --as martin create pod -n dev-z
no
root@controlplane:/# k auth can-i --as martin list pod -n dev-z
yes
root@controlplane:/# k auth can-i --as martin get pod -n dev-z
yes
```


#### Mock 2 (Ques 6)

On the controlplane node, an unknown process is bound to the port 8088. Identify the process and prevent it from running again by stopping and disabling any associated services. Finally, remove the package that was responsible for starting this process.

port 8088 free ?
associated service stopped and disabled?
associated package removed?

```
  65  ss -tunlp | grep 8088
   66  ps -ef | grep 30388
   67  systemctl status lshttpd.service
   68  cat /etc/systemd/system/lshttpd.service;
   69  systemctl stop lshttpd.service
   70  systemctl disable lshttpd.service
   71  ss -tunlp | grep 8088
   72  dpkg -S /usr/local/lsws/bin/lswsctrl
   73  apt purge openlitespeed:
   74  apt purge openlitespeed
   75  ls /usr/local/lsws
   76  ls /usr/local/lsws/b
   77  ls /usr/local/
   78  history
```

#### Mock 2 (Ques 7)

A pod has been created in the omega namespace using the pod definition file located at /root/CKS/omega-app.yaml. However, there is something wrong with it and the pod is not in a running state.

We have used a custom seccomp profile located at /var/lib/kubelet/seccomp/custom-profile.json to ensure that this pod can only make use of limited syscalls to the Linux Kernel of the host operating system. However, it appears the profile does not allow the read and write syscalls. Fix this by adding it to the profile and use it to start the pod.

pod running?
pod uses the correct seccomp profile?
seccomp profile allows 'read' and 'write' syscalls?


```
cat /root/CKS/omega-app.yaml
apiVersion: v1
kind: Pod
metadata:
    labels:
      app: omega-app
    name: omega-app
    namespace: omega
spec:
    containers:
    - args:
      - -text=just made some syscalls!
      image: hashicorp/http-echo:0.2.3
      imagePullPolicy: IfNotPresent
      name: test-container
      resources: {}
      securityContext:
        allowPrivilegeEscalation: false
    dnsPolicy: ClusterFirst
    enableServiceLinks: true
    preemptionPolicy: PreemptLowerPriority
    priority: 0
    restartPolicy: Always
    schedulerName: default-scheduler
    securityContext:
      seccompProfile:
        localhostProfile: custom-profile.json
        type: Localhost
    serviceAccount: default
    serviceAccountName: default
```


#### Mock 2 (Ques 8)

A pod definition file has been created at /root/CKS/simple-pod.yaml . Using the kubesec tool, generate a report for this pod definition file and fix the major issues so that the subsequent scan report no longer fails.

Once done, generate the report again and save it to the file /root/CKS/kubesec-report.txt

pod definition file fixed?
report generated at /root/CKS/kubesec-report.txt ?


```
cat /root/CKS/simple-pod.yaml
apiVersion: v1
kind: Pod
metadata:
    labels:
        name: simple-webapp
    name: simple-webapp-1
spec:
    containers:
        -
            image: kodekloud/webapp-delayed-start
            name: simple-webapp
            ports:
                -
                    containerPort: 8080
            securityContext:
                capabilities:
                    add:
                        - NET_ADMIN
                        # - SYS_ADMIN         <<< - remove this line

   98  kubesec scan  /root/CKS/simple-pod.yaml
   99  kubesec scan  /root/CKS/simple-pod.yaml > /root/CKS/kubesec-report.txt
```

#### Mock 2 (Ques 9)

Create a new pod called secure-nginx-pod in the seth namespace. Use one of the images from the below which has a least number of CRITICAL vulnerabilities.

nginx
nginx:1.19
nginx:1.17
nginx:1.20
gcr.io/google-containers/nginx
bitnami/nginx:latest


```
for i in nginx nginx:1.19 nginx:1.17 nginx:1.20 gcr.io/google-containers/nginx bitnami/nginx:latest; do echo "trivy --severity=CRITICAL  i $i | grep -i Total # $i" ; done
```
