---
# intentionally left blank
title: Ansible Bitbucket
date: 2024-10-04T20:14:27+0200
lastmod: 2024-10-04T20:14:27+0200
draft: false
description: "How to automate Bitbucket project and repository creation, including permissions management, using Ansible URI module."
image: "https://miro.medium.com/v2/0*sV8pi5txXJiFOJfJ.png"
author: "Jan Toth"
tags: ['bash', 'devopsinuse']
categories: ["Linux"]
---

The following Ansible playbook automates common Bitbucket administration tasks. It reads a YAML definition file, creates a Bitbucket project, grants group-level permissions, imports a repository from a sample project URL, and assigns user-level permissions. This is useful when onboarding new projects where you need repeatable, automated Bitbucket setup.

```yaml

# .........................................................................
# 1. Creating Bitbucket project for GCP Solution Project
# .........................................................................
- name: "Read yaml file"
  ansible.builtin.shell: "cat {{ DEFINITION_FILE }}"
  register: result

- name: "Parse yaml into variable"
  set_fact:
    feed: "{{ result.stdout | from_yaml }}"

- name: creating Bitbucket project for GCP Solution Project
  uri:
    url: "{{ BITBUCKET_URL }}/rest/api/latest/projects"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Content-Type: "application/json"
      Accept: "application/json"
    method: POST
    body:
      key: "{{ feed.vcs_project }}"
    body_format: json
    validate_certs: False
    status_code: [200, 201, 409]
  register: _response

# .........................................................................
# 2. Granting PROJECT_ADMIN to ed pas horizon group at Bitbucket project level
# .........................................................................
- name: Grant permissions to ed pas horizon
  uri:
    url: "{{ BITBUCKET_URL }}/rest/api/latest/projects/{{ feed.vcs_project }}/permissions/groups?name={{ HORZION_GROUP | urlencode }}&permission=PROJECT_ADMIN"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Accept: "application/json"
    method: PUT
    validate_certs: False
    status_code: [200, 201, 204]
  register: _response

# .........................................................................
# 3. Import/create new repo with sample code
# .........................................................................
- name: import/create new repo with sample code
  uri:
    url: "{{ BITBUCKET_URL }}/rest/importer/latest/projects/{{ feed.vcs_project }}/import/repos"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Content-Type: "application/json"
      Accept: "application/json"
    method: POST
    body:
      externalRepositories:
        - cloneUrl: "{{ SAMPLE_PROJECT_URL }}"
          name: "{{ feed.vcs_repo }}"
          scmId: "git"
    body_format: json
    validate_certs: False
    status_code: [200, 201, 409]
  register: _response

# .........................................................................
# 4. Grant necessary permissions to Bitbucket repo
# .........................................................................
- name: construct permissions query string
  set_fact:
    permissions_query: >
      permission=REPO_ADMIN
      {% for item in feed.vcs_admins %}
      &name={{ item | urlencode }}
      {% endfor %}

- name: grant necessary permissions to Bitbucket repo REPO_ADMIN
  uri:
    url: "{{ BITBUCKET_URL }}/rest/api/latest/projects/{{ feed.vcs_project }}/repos/{{ feed.vcs_repo }}/permissions/users?{{ permissions_query }}"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Content-Type: "application/json"
      Accept: "application/json"
    method: PUT
    body_format: form-urlencoded
    validate_certs: False
    status_code: [200, 201, 204]
  register: _response


```
