---
title: "How to print Jenkins credentials from the Script Console"
date: 2026-03-31T09:00:00+0200
lastmod: 2026-03-31T09:00:00+0200
draft: false
description: "Retrieve and print stored Jenkins credentials using a Groovy script in the Jenkins Script Console, useful for debugging and auditing credential configurations."
image: "https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=800&h=420&fit=crop"
author: "Jan Toth"
tags: ['jenkins', 'groovy']
categories: ["DevOps"]
---

Sometimes you need to verify which credentials are actually stored in Jenkins — for example, when a pipeline fails with an authentication error and you want to confirm the credential ID exists and has the expected values. The **Jenkins Script Console** (`Manage Jenkins → Script Console`) lets you run arbitrary Groovy code on the controller, making it the quickest way to inspect credentials without clicking through the UI.

> **Security warning**: The Script Console has full access to the Jenkins JVM. Only administrators should have access to it, and you should never run untrusted scripts. Printed secrets will appear in your browser — make sure no one is looking over your shoulder.
{: .prompt-warning }

## The Groovy script

Navigate to `Manage Jenkins → Script Console` and paste the following:

```groovy
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.common.*
import com.cloudbees.plugins.credentials.domains.*
import jenkins.model.*

// Get the credentials store
def store = Jenkins.instance.getExtensionList(
    'com.cloudbees.plugins.credentials.SystemCredentialsProvider'
)[0].getStore()

// Find your credential by ID
def credsId = "TFE_TOKEN_..."
def creds = com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.instance,
    null,
    null
).find { it.id == credsId }

// Print the credential details
if (creds) {
    println "Credential ID: ${creds.id}"
    println "Description: ${creds.description}"
    if (creds instanceof com.cloudbees.plugins.credentials.common.StandardUsernameCredentials) {
        println "Username: ${creds.username}"
    }
    if (creds instanceof com.cloudbees.plugins.credentials.common.StandardUsernamePasswordCredentials) {
        println "Password: ${creds.password}"
    }
    if (creds instanceof com.cloudbees.plugins.credentials.common.StandardCredentials
        && creds.hasProperty('secret')) {
        println "Secret: ${creds.secret}"
    }
} else {
    println "Credential not found"
}
```

## How it works

1. **Imports** — the `com.cloudbees.plugins.credentials` packages are provided by the [Credentials Plugin](https://plugins.jenkins.io/credentials/), which is installed on virtually every Jenkins instance.
2. **`lookupCredentials`** — searches the global domain for any credential matching the `StandardCredentials` interface, then filters by ID.
3. **Type checks** — Jenkins stores different credential types (username/password, secret text, SSH key, etc.). The `instanceof` checks ensure you only call methods that exist on the actual type:
   - `StandardUsernameCredentials` → has `.username`
   - `StandardUsernamePasswordCredentials` → has `.password`
   - Secret text credentials expose a `.secret` property

Replace `"TFE_TOKEN_..."` with the actual credential ID you want to inspect. The output will look something like:

```text
Credential ID: TFE_TOKEN_myproject
Description: Terraform Enterprise token for myproject
Secret: s.ABcdEf1234567890xyzW
```

## Listing all credentials

If you don't know the exact credential ID, you can list every credential in the global store:

```groovy
import com.cloudbees.plugins.credentials.*
import com.cloudbees.plugins.credentials.common.*
import jenkins.model.*

com.cloudbees.plugins.credentials.CredentialsProvider.lookupCredentials(
    com.cloudbees.plugins.credentials.common.StandardCredentials.class,
    Jenkins.instance,
    null,
    null
).each {
    println "${it.id} (${it.class.simpleName}) - ${it.description}"
}
```

This prints every credential ID, its Java type, and description — handy for auditing what is configured before you narrow down to a specific one.
