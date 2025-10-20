---
title: "OPA - Gatekeeper"
date: 2022-06-03T14:25:17+02:00
lastmod: 2022-01-24T15:03:56+01:00
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Open Policy Agent - Gatekeeper"

tags: ['opa', 'gatekeeper']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---


* OPA is not Kubenretes specific
* general purpose policy engine
* An admission controller is a piece of code that intercepts requests to the Kubernetes API server prior to persistence of the object, but after the request is authenticated and authorized.
* Leveraging Rego language
* works with JSON/YAML
* in Kubernetes it uses Admission Controllers
* does not know anything about concepts like pods or deployments
* OPA Gatekeeper (with Custom Resource Definitions)

![Image](/assets/images/blog/opa-1.png)

##### How it works

* create `ConstraintTemplate`

![Image](/assets/images/blog/opa-2.png)

###### Install Gatekeeper OPA to your cluster

Thanks to [Dynamic Admission Controller](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) there is no need to configure `kube-api` server.

There are two kinds of `webhooks`:

* `validating` admission webhook
* `mutating` admission webhook

```python
kubectl create -f https://raw.githubusercontent.com/killer-sh/cks-course-environment/master/course-content/opa/gatekeeper.yaml

# Check what was created in gatekeeper-system namespace
 k get pod,svc -n gatekeeper-system
NAME                                                 READY   STATUS    RESTARTS   AGE
pod/gatekeeper-audit-65f658df68-rfg4j                1/1     Running   0          62s
pod/gatekeeper-controller-manager-5fb6c9ff69-vqqxj   1/1     Running   0          62s

NAME                                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/gatekeeper-webhook-service   ClusterIP   10.103.249.167   <none>        443/TCP   62s

```

###### Create your first template

**ConstraintTemplate**: `allwaysdeny_template`

```yaml
cat <<'EOF' > alwaysdeny_template.yaml
---
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8salwaysdeny
spec:
  crd:
    spec:
      names:
        kind: K8sAlwaysDeny
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          properties:
            message:
              type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8salwaysdeny
        violation[{"msg": msg}] {
          1 > 0
          msg := input.parameters.message
        }
EOF
```

A new Custom Resource Definition called `K8sAlwaysDeny` will be created

```
root@scw-k8s-cks:~# k get crd
NAME                                                 CREATED AT
configs.config.gatekeeper.sh                         2022-01-24T14:44:30Z
constraintpodstatuses.status.gatekeeper.sh           2022-01-24T14:44:30Z
constrainttemplatepodstatuses.status.gatekeeper.sh   2022-01-24T14:44:30Z
constrainttemplates.templates.gatekeeper.sh          2022-01-24T14:44:30Z

# Run kubectl create -f ...
root@scw-k8s-cks:~# k create -f  alwaysdeny_template.yaml
constrainttemplate.templates.gatekeeper.sh/k8salwaysdeny created

# Check a new Custom Resource Definition k8salwaysdeny.constraints.gatekeeper.sh
root@scw-k8s-cks:~# k get crd
NAME                                                 CREATED AT
configs.config.gatekeeper.sh                         2022-01-24T14:44:30Z
constraintpodstatuses.status.gatekeeper.sh           2022-01-24T14:44:30Z
constrainttemplatepodstatuses.status.gatekeeper.sh   2022-01-24T14:44:30Z
constrainttemplates.templates.gatekeeper.sh          2022-01-24T14:44:30Z
k8salwaysdeny.constraints.gatekeeper.sh              2022-01-24T15:05:08Z

```

###### Now create that `k8salwaysdeny.constraints.gatekeeper.sh`

```yaml
cat <<'EOF' > all_pod_always_deny.yaml

apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAlwaysDeny
metadata:
  name: pod-always-deny
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    message: "ACCESS DENIED!"
EOF
```

Apply this file ...

```
# Kubectl it ...
root@scw-k8s-cks:~# kubectl  create -f all_pod_always_deny.yaml
k8salwaysdeny.constraints.gatekeeper.sh/pod-always-deny created
```

Now, we should not be able to create any pod since `1>0` in Rego language

```
root@scw-k8s-cks:~# k run podx --image=nginx
Error from server ([pod-always-deny] ACCESS DENIED!): admission webhook "validation.gatekeeper.sh" denied the request: [pod-always-deny] ACCESS DENIED!
```

##### Require labels on namespaces and pods

To achieve such a goal we need to create `ConstraintTemplate` first with some appropriate `Rego` code.


```

cat <<'EOF' > k8srequiredlabels_template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
spec:
  crd:
    spec:
      names:
        kind: K8sRequiredLabels
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          properties:
            labels:
              type: array
              items: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8srequiredlabels
        violation[{"msg": msg, "details": {"missing_labels": missing}}] {
          provided := {label | input.review.object.metadata.labels[label]}
          required := {label | label := input.parameters.labels[_]}
          missing := required - provided
          count(missing) > 0
          msg := sprintf("you must provide labels: %v", [missing])
        }
EOF

# kubectl create this file
root@scw-k8s-cks:~# k create -f k8srequiredlabels_template.yaml
constrainttemplate.templates.gatekeeper.sh/k8srequiredlabels created

```

Same with all namespaces. We need to change only `K8sRequiredLabels` Custom Resource Definition.

```yaml
cat <<'EOF' > k8srequiredlabels_on_namespaces.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: ns-must-have-cks
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Namespace"]
  parameters:
    labels: ["cks"]
EOF
```

Then create `K8sRequiredLabels` Custom Resource Definition to ensure POD have some labels.


```yaml
cat <<'EOF' > all_pod_must_have_cks.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sRequiredLabels
metadata:
  name: pod-must-have-cks
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
  parameters:
    labels: ["cks"]
EOF
```


Make sure to apply both files and by now we should have labels `cks` enforced on both `PODS` and `namespaces`.

```
root@scw-k8s-cks:~# k create -f all_pod_must_have_cks.yaml
k8srequiredlabels.constraints.gatekeeper.sh/pod-must-have-cks created
root@scw-k8s-cks:~# k create -f k8srequiredlabels_on_namespaces.yaml
k8srequiredlabels.constraints.gatekeeper.sh/ns-must-have-cks created

```

Let's try to create some **namespace**

```
root@scw-k8s-cks:~# k create ns new-namespace
Error from server ([ns-must-have-cks] you must provide labels: {"cks"}): admission webhook "validation.gatekeeper.sh" denied the request: [ns-must-have-cks] you must provide labels: {"cks"}

```


###### Restrict number of `replicaCount`


```yaml
cat <<'EOF' > k8sminreplicacount_template.yaml
apiVersion: templates.gatekeeper.sh/v1beta1
kind: ConstraintTemplate
metadata:
  name: k8sminreplicacount
spec:
  crd:
    spec:
      names:
        kind: K8sMinReplicaCount
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          properties:
            min:
              type: integer
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sminreplicacount
        violation[{"msg": msg, "details": {"missing_replicas": missing}}] {
          provided := input.review.object.spec.replicas
          required := input.parameters.min
          missing := required - provided
          missing > 0
          msg := sprintf("you must provide %v more replicas", [missing])
        }
EOF
```

Then object create `K8sMinReplicaCount`

```yaml

cat <<'EOF' > all_deployment_must_have_min_replicacount.yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sMinReplicaCount
metadata:
  name: deployment-must-have-min-replicas
spec:
  match:
    kinds:
      - apiGroups: ["apps"]
        kinds: ["Deployment"]
  parameters:
    min: 2
EOF
```

Create new Custom Resource Definitions

```
# kubectl create ...
kubectl create -f k8sminreplicacount_template.yaml
kubectl create -f all_deployment_must_have_min_replicacount.yaml

```

Test replicaCount restriction


```
root@scw-k8s-cks:~# k create  deployment test  --image=nginx  -oyaml --dry-run=client > deployment.yaml
root@scw-k8s-cks:~# vim deployment.yaml
root@scw-k8s-cks:~# k create -f  deployment.yaml
Error from server ([deployment-must-have-min-replicas] you must provide 1 more replicas): error when creating "deployment.yaml": admission webhook "validation.gatekeeper.sh" denied the request: [deployment-must-have-min-replicas] you must provide 1 more replicas
```

##### Rego playground
https://play.openpolicyagent.org/


![Image](/assets/images/blog/opa-4.png)


###### Old way - creating a `configMap` with a special label and in a special namespace

```yaml
 kubectl  get cm unique-host -o yaml
apiVersion: v1
data:
  unique-host.rego: |
    package kubernetes.admission
    import data.kubernetes.ingresses

    deny[msg] {
        some other_ns, other_ingress
        input.request.kind.kind == "Ingress"
        input.request.operation == "CREATE"
        host := input.request.object.spec.rules[_].host
        ingress := ingresses[other_ns][other_ingress]
        other_ns != input.request.namespace
        ingress.spec.rules[_].host == host
        msg := sprintf("invalid ingress host %q (conflicts with %v/%v)", [host, other_ns, other_ingress])
    }
kind: ConfigMap
metadata:
  annotations:
    openpolicyagent.org/policy-status: '{"status":"ok"}'
  creationTimestamp: "2021-05-01T12:37:05Z"
  labels:
    openpolicyagent.org/policy: rego
  name: unique-host
  namespace: opa

```
