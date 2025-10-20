---
title: "Game of Pods - Voting app"
date: "2022-01-06T14:53:42+0100"
lastmod: "2022-01-06T14:53:42+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/kubernetes-cert-1.png"
description: "Game of Pods - Voting app"

tags: ['game', 'of', 'pods', 'voting', 'app']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```yaml
for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
filename: db-depl.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: db-deployment
  name: db-deployment
  namespace: vote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: db-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: db-deployment
    spec:
      volumes:
      - name: db-data
        emptyDir: {}
      containers:
      - image: postgres:9.4
        name: postgres
        resources: {}
        env:
        - name: POSTGRES_PASSWORD
          value: "password"
        volumeMounts:
        - name: db-data
          mountPath: '/var/lib/postgresql/data'
status: {}
filename: redis-deployment.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: redis-deployment
  name: redis-deployment
  namespace: vote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-deployment
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: redis-deployment
    spec:
      volumes:
      - name: redis-data
        emptyDir: {}
      containers:
      - image: redis:alpine
        name: redis
        resources: {}
        volumeMounts:
        - name: redis-data
          mountPath: "/data"
status: {}
filename: vote-svc.yaml
---
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: null
  labels:
    app: vote-deployment
  name: vote-service
  namespace: vote
spec:
  ports:
  - port: 5000
    protocol: TCP
    targetPort: 80
    nodePort: 31000
  selector:
    app: vote-deployment
  type: NodePort
status:
  loadBalancer: {}
filename: worker-dep.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: worker
  name: worker
  namespace: vote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: worker
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: worker
    spec:
      containers:
      - image: kodekloud/examplevotingapp_worker
        name: examplevotingapp-worker
        resources: {}
status: {}
filename: worker.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: worker
  name: worker
  namespace: vote
spec:
  replicas: 1
  selector:
    matchLabels:
      app: worker
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: worker
    spec:
      containers:
      - image: kodekloud/examplevotingapp_worker
        name: examplevotingapp-worker
        resources: {}
status: {}
```

```
e deployment worker --image=kodekloud/examplevotingapp_worker -o yaml --dry-run=client
    4  kubectl  create deployment worker --image=kodekloud/examplevotingapp_worker -o yaml --dry-run
    5  kubectl  create deployment worker --image=kodekloud/examplevotingapp_worker -o yaml --dry-run > worker.yaml
    6  vim worker.yaml
    7  kubectl apply -f  worker.yaml
    8  vim worker.yaml
    9  kubectl apply -f  worker.yaml
   10  kubectl  get pods
   11  kubectl  logs -f worker-764f87c697-2qxpf
   12  kubectl  get pods
   13  kubectl  delete  pod worker-764f87c697-2qxpf
   14  vim worker.yaml
   15  kubectl  get ns
   16  kubectl  create -n vote-ns
   17  kubectl  create namespace vote-ns
   18  kubectl  create -f worker.yaml
   19  kubectl  get pod -A
   20  kubectl  delete pod worker-764f87c697-ldk66
   21  kubectl  get pods -n kube-system
   22  kubectl  get nodes
   23  kubectl  create deployment redis-deployment --help
   24  kubectl  create deployment redis-deployment --image=redis:alpine --help
   25  kubectl  create deployment redis-deployment --image=redis:alpine --dry-run -o yaml
   26  kubectl  create deployment redis-deployment --image=redis:alpine --dry-run -o yaml > redis-deployment.yaml
   27  vim redis-deployment.yaml
   28  kubectl create -f redis-deployment.yaml
   29  vim redis-deployment.yaml
   30  kubectl create -f redis-deployment.yaml
   31  kubectl  get pods -n vote-ns
   32  kubectl  create ns vote
   33  kubectl  delete -f redis-deployment.yaml
   34  kubectl  delete -f worker.yaml
   35  vim redis-deployment.yaml
   36  vim worker.yaml
   37  kubectl  create -f redis-deployment.yaml
   38  kubectl  get pods -n vote-ns
   39  kubectl  get pods -n vote
   40  kubectl  expose   deployment -n vote redis-deployment --port=6379 --target-port=6379 --type=ClusterIP
   41  kubectl  get svc -n vote
   42  kubectl  delete svc redis-deployment -n vote
   43  kubectl  expose   deployment -n vote redis-deployment --port=6379 --target-port=6379 --type=ClusterIP --name=redis
   44  kubectl  create deployment vote-deployment --image=kodekloud/examplevotingapp_vote:before
   45  kubectl  create deployment vote-deployment --image="kodekloud/examplevotingapp_vote:before"
   46  kubectl  create deployment vote-deployment --image="kodekloud/examplevotingapp-vote:before"
   47  kubectl  delete  deployments vote-deployment
   48  kubectl  create deployment vote-deployment --image="kodekloud/examplevotingapp-vote:before" -n vote
   49  kubectl  get deployments -n vote
   50  kubectl  get pods -n vote
   51  kubectl  edit deployments -n vote vote-deployment
   52* kubectl  get pods -n vote
   53  kubectl  expose  deployment  -n vote vote-deployment --port=5000 --target-port=80 --type=NodePort --name=vote-service --dry-run=client -o yaml
   54  kubectl  expose  deployment  -n vote vote-deployment --port=5000 --target-port=80 --type=NodePort --name=vote-service --dry-run -o yaml
   55  kubectl  expose  deployment  -n vote vote-deployment --port=5000 --target-port=80 --type=NodePort --name=vote-service --dry-run -o yaml > vote-svc.yaml
   56  vim vote-svc.yaml
   57  kubectl create -f  vote-svc.yaml
   58  kubectl  create deployment worker --image='kodekloud/examplevotingapp_worker' --dry-run -o yaml
   59  kubectl  create deployment worker --image='kodekloud/examplevotingapp_worker' --dry-run -o yaml > worker-dep.yaml
   60  vim worker-dep.yaml
   61  kubectl create -f  worker-dep.yaml
   62  kubectl  get pods -n vote
   63  kubectl  describe pod worker-764f87c697-sf746 -n vote
   64  vim worker-dep.yaml
   65  kubectl  describe deployments worker
   66  kubectl  get pods -n vote
   67  kubectl  logs -f worker-764f87c697-sf746 -n vote
   68  kubectl  logs -f worker-764f87c697-9r6z2  -n vote
   69  kubectl  create service clusterip db --help
   70  kubectl  create service clusterip db --tcp=5432:5432
   71  kubectl  delete  svc db
   72  kubectl  create service clusterip db --tcp=5432:5432 --namespace=vote
   73  kubectl create deployment db-deployment --image='postgres:9.4' --namespace=vote --dry-run -o yaml
   74  kubectl create deployment db-deployment --image='postgres:9.4' --namespace=vote --dry-run -o yaml > db-depl.yaml
   75  vim db-depl.yaml
   76  kubectl create -f  db-depl.yaml
   77  kubectl  get pods -n vote
   78  watch kubectl  get pods -n vote
   79  kubectl  logs -f db-deployment-75db6d6859-5fkfn -n vote
   80  kubectl delete -f  db-depl.yaml
   81  vim db-depl.yaml
   82  kubectl create -f  db-depl.yaml
   83  watch kubectl  get pods -n vote
   84  kubectl  delete svc -n vote db
   85  kubectl  expose deployment -n vote db-deployment --port=5432 --target-port=5432
   86  kubectl  delete svc -n vote db
   87  kubectl  delete svc -n vote vote-service
   88  kubectl  expose deployment -n vote db-deployment --port=5432 --target-port=5432 --name=db
   89  kubectl  expose deployment -n vote vote-deployment --port=5000 --target-port=80 --name=vote-service --type=NodePort
   90  kubectl  edit svc -n vote vote-service
   91  kubectl  create deployment result-deployment --image='kodekloud/examplevotingapp_result:before'
   92  kubectl  create deployment result-deployment --image='kodekloud/examplevotingapp-result:before' -n vote
   93  kubectl  get deployments.
   94  kubectl  get deployments
   95  kubectl  get deployments -n vote
   96  kubectl edit deployments result-deployment  -n vote
   97  kubectl  get pod -n vote
   98  kubectl edit deployments result-deployment  -n vote
   99  kubectl  get pod -n vote
  100  kubectl  expose deployment -n vote result-deployment --port=5001 --target-port=80 --name=result-service --type=NodePort
  101  kubectl  edit svc -n vote result-service
  102  for i in $(ls *.yaml); do echo filename: $i;echo "---" ;cat $i; done
  103  history
```
