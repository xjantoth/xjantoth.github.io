---
title: "How to Jenkins seed files"
date: 2022-03-15T08:59:30+0100
lastmod: 2022-03-15T08:59:30+0100
draft: false
description: "Jenkins seed"
image: "assets/images/blog/linux-1.jpg"
author: "Jan Toth"
tags:
  - jenkins
  - seed
---


```
sudo nerdctl run --name jenkins -p 8080:8080 -v $PWD/initial.xml:/var/jenkins_home/jobs/seed/config.xml -v $PWD/controller-configuration-jobDSL-orig.yaml:/var/jenkins.yaml -d --env JENKINS_ADMIN_PASSWORD=password jenkins:jobdsl-blog-2

```

Basic Seed job that creates a definitions for other jobs

```
pipelineJob("${SEED_PROJECT}-${SEED_BRANCH}-tf-enterprise") {
    description "Terraform enterprise the ${BRANCH} branch."
    // because stash notifier will not work



    triggers {
        scm('')
    }

    logRotator {
        numToKeep(5)
        artifactNumToKeep(1)
    }

    definition {
        cpsScm {
            scm {
                git{
                    remote {
                        url("${PROJECT_SCM_URL}")
                        credentials("BITBUCKET_SSH_KEY_SECURITY")
                    }
                    branches("${BRANCH}")
                    extensions { }

                }
            scriptPath('Jenkinsfile-tfe')


            }
        }
}
}

pipelineJob("${SEED_PROJECT}-${SEED_BRANCH}-builddeploy") {
    description "Building and deploying the ${BRANCH} branch."
    // because stash notifier will not work



    triggers {
        scm('')
    }

    logRotator {
        numToKeep(5)
        artifactNumToKeep(1)
    }

    definition {
        cpsScm {
            scm {
                git{
                    remote {
                        url("${PROJECT_SCM_URL}")
                        credentials("BITBUCKET_SSH_KEY_SECURITY")
                    }
                    branches("${BRANCH}")
                    extensions { }

                }
            scriptPath('Jenkinsfile')


            }
        }
}
}
```

An example of `Jenkinsfile`



```

pipeline {
    agent any

    stages {
        stage('Terraform init') {
            steps {

                  withCredentials([string(credentialsId: 'ARM_CLIENT_ID', variable: 'ARM_CLIENT_ID'), string(credentialsId: 'ARM_CLIENT_SECRET', variable: 'ARM_CLIENT_SECRET'), string(credentialsId: 'ARM_TENANT_ID', variable: 'ARM_TENANT_ID'), string(credentialsId: 'ARM_SUBSCRIPTION_ID', variable: 'ARM_SUBSCRIPTION_ID'), ]) {
                    sh '''
                      set +x
                      echo $ARM_SUBSCRIPTION_ID
                      export ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID
                      export ARM_TENANT_ID=$ARM_TENANT_ID
                      export ARM_CLIENT_ID=$ARM_CLIENT_ID
                      export ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET

                      cd terraform
                      terraform init
                    '''
                  }

            }
        }

        stage('Terraform validate') {
            steps {

                  withCredentials([string(credentialsId: 'ARM_CLIENT_ID', variable: 'ARM_CLIENT_ID'), string(credentialsId: 'ARM_CLIENT_SECRET', variable: 'ARM_CLIENT_SECRET'), string(credentialsId: 'ARM_TENANT_ID', variable: 'ARM_TENANT_ID'), string(credentialsId: 'ARM_SUBSCRIPTION_ID', variable: 'ARM_SUBSCRIPTION_ID'), ]) {
                    sh '''
                      set +x
                      echo $ARM_SUBSCRIPTION_ID
                      export ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID
                      export ARM_TENANT_ID=$ARM_TENANT_ID
                      export ARM_CLIENT_ID=$ARM_CLIENT_ID
                      export ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET

                      cd terraform
                      terraform validate
                    '''
                  }

            }
        }
        stage('Terraform plan') {
            steps {

                  withCredentials([string(credentialsId: 'ARM_CLIENT_ID', variable: 'ARM_CLIENT_ID'), string(credentialsId: 'ARM_CLIENT_SECRET', variable: 'ARM_CLIENT_SECRET'), string(credentialsId: 'ARM_TENANT_ID', variable: 'ARM_TENANT_ID'), string(credentialsId: 'ARM_SUBSCRIPTION_ID', variable: 'ARM_SUBSCRIPTION_ID'), ]) {
                    sh '''
                      set +x
                      echo $ARM_SUBSCRIPTION_ID
                      export ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID
                      export ARM_TENANT_ID=$ARM_TENANT_ID
                      export ARM_CLIENT_ID=$ARM_CLIENT_ID
                      export ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET

                      cd terraform
                      terraform plan
                    '''
                  }

            }
        }

        stage('Approval to proceed with terraform apply') {

            input { message "Terraform has been initialized! When hitting proceed terraform will run code in Cloud!!!"}
            steps {
                echo "Terraform has been initialized and planned!"
            }
        }

        stage('Terraform apply') {
            steps {

                  withCredentials([string(credentialsId: 'ARM_CLIENT_ID', variable: 'ARM_CLIENT_ID'), string(credentialsId: 'ARM_CLIENT_SECRET', variable: 'ARM_CLIENT_SECRET'), string(credentialsId: 'ARM_TENANT_ID', variable: 'ARM_TENANT_ID'), string(credentialsId: 'ARM_SUBSCRIPTION_ID', variable: 'ARM_SUBSCRIPTION_ID'), ]) {
                    sh '''
                      set +x
                      echo $ARM_SUBSCRIPTION_ID
                      export ARM_SUBSCRIPTION_ID=$ARM_SUBSCRIPTION_ID
                      export ARM_TENANT_ID=$ARM_TENANT_ID
                      export ARM_CLIENT_ID=$ARM_CLIENT_ID
                      export ARM_CLIENT_SECRET=$ARM_CLIENT_SECRET

                      cd terraform
                      terraform apply -auto-approve -var-file terraform.tfvars
                    '''
                  }

            }

        }
    }
}
```
