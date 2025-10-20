---
title: How to create resource in Bitbucket via curl and Ansible
date: 2024-07-25T09:39:30+0200
lastmod: 2024-07-25T09:39:30+0200
draft: false
description: How to create resource in Bitbucket via curl and Ansible
image: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR4sLbHPgMQ6s1WLgCB-6JUcjlftThBFl-OdQ&s
author: "Jan Toth"
tags:
  - bash
  - devopsinuse
  - curl
  - ansible
---

There are some situation when one can have credentials to some web page that does not have API properly exposed and TOKEN can not be used.
However, when trying to do certain action e.g. import Bitbucket repo from already existing repo - this is doable by `clicking` in `a web browser` using
username and password. In this particular situation the reference/sample code can be found in variable `SAMPLE_PROJECT_URL`.

In this case one can take an advantage of cookies and trying to simulate a browser.

```bash
export PASSWORD='...'
export USERNAME='...'
export BB_PROJECT_NAME="PROJECT-NAME"
export BITBUCKET_REPO_NAME="REPO-NAME"
export SAMPLE_PROJECT_URL="https://example.net/scm/example-solutions/sample-valid.git"

# repo level
export WRITERS="<username1> <username2> ..."
export ADMINS="<username4> <username5> ..."

echo -e "\n\nCreting a project\n"

curl -u "${USERNAME}:${PASSWORD}" -k --url "https://bitbucket.url.example/rest/api/latest/projects" \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
  "key": "'"${BB_PROJECT_NAME}"'"
}'

echo -e "\n\nGET a project\n"

curl -u "${USERNAME}:${PASSWORD}" -k --url 'https://bitbucket.url.example/rest/api/latest/projects/'"${BB_PROJECT_NAME}"'' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json'

echo -e "\n\nGrant permissions to ed pas horizon\n"

curl -u "${USERNAME}:${PASSWORD}" -k --request PUT \
  --url 'https://bitbucket.url.example/rest/api/latest/projects/'"${BB_PROJECT_NAME}"'/permissions/groups' \
  --header 'Accept: application/json' \
  --url-query "name=<group-name>" \
  --url-query "permission=PROJECT_ADMIN"

# ............................................
# Import/crate new repo with sample code
# ............................................

rm /tmp/cookies.txt
curl -G -k -c - 'https://bitbucket.url.example/j_atl_security_check' \
  -H "Content-Type: application/x-www-form-urlencoded; Charset=utf-8" \
  --data-urlencode "j_username=${USERNAME}" \
  --data-urlencode "j_password=${PASSWORD}" \
  --data-urlencode "queryString=native_login=" \
  --data-urlencode "submit=Log in" > /tmp/cookies.txt

curl -k  -b /tmp/cookies.txt 'https://bitbucket.url.example/rest/importer/latest/projects/'"${BB_PROJECT_NAME}"'/import/repos' \
  --header 'Content-Type: application/json' \
  --data '{
    "externalRepositories":[{
      "cloneUrl":"'"${SAMPLE_PROJECT_URL}"'",
      "name":"'"${BITBUCKET_REPO_NAME}"'",
      "scmId":"git"
    }]
  }'


# echo -e "\n\nCreate repository\n"

# curl -u "${USERNAME}:${PASSWORD}" -k --url 'https://bitbucket.url.example/rest/api/1.0/projects/'"${BB_PROJECT_NAME}"'/repos' \
# --header 'Accept: application/json' \
# --header 'Content-Type: application/json' \
# --data '{
#   "name": "'"${BITBUCKET_REPO_NAME}"'",
#   "project": {
#     "key": "'"${BB_PROJECT_NAME}"'"
#   },
#   "slug": "'"${BITBUCKET_REPO_NAME}"'",
#   "scmId": "git"
# }'

echo -e "\n\nGrant users WRITE permissions\n"

curl  -k -X PUT \
-u "${USERNAME}:${PASSWORD}" \
--url 'https://bitbucket.url.example/rest/api/latest/projects/'"${BB_PROJECT_NAME}"'/repos/'"${BITBUCKET_REPO_NAME}"'/permissions/users' \
--header 'Accept: application/json' --header 'Content-Type: application/json' $(for i in $(echo $WRITERS); do echo -n --url-query name=$i" " ; done) \
--url-query "permission=REPO_WRITE"

echo -e "\n\nGrant users ADMIN permissions\n"

curl  -k -X PUT \
-u "${USERNAME}:${PASSWORD}" \
--url 'https://bitbucket.url.example/rest/api/latest/projects/'"${BB_PROJECT_NAME}"'/repos/'"${BITBUCKET_REPO_NAME}"'/permissions/users' \
--header 'Accept: application/json' --header 'Content-Type: application/json' $(for i in $(echo $ADMINS); do echo -n --url-query name=$i" " ; done) \
--url-query "permission=REPO_ADMIN"
```


## Ansible version

```bash
---
# .........................................................................
# 1. Creating Bitbucket project
# .........................................................................
- name: Read input YAML file
  ansible.builtin.shell: cat {{ DEFINITION_FILE }}
  register: result

- name: Load input data into data variable
  set_fact:
    data: "{{ result.stdout | from_yaml }}"

- name: Create Bitbucket project
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
      key: "{{ data.bb_project }}"
    body_format: json
    validate_certs: no
    status_code: [200, 201, 409]
  register: response

# .........................................................................
# 2. Granting PROJECT_ADMIN to BB_GROUP_NAME group at Bitbucket project level
# .........................................................................
- name: Grant permissions to group BB_GROUP_NAME
  uri:
    url: "{{ BITBUCKET_URL }}/rest/api/latest/projects/{{ data.bb_project }}/permissions/groups?name={{ BB_GROUP_NAME | urlencode }}&permission=PROJECT_ADMIN"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Accept: "application/json"
    method: PUT
    validate_certs: no
    status_code: [200, 201, 204]
  register: response

# .........................................................................
# 3. Import/create new repo with sample code
# .........................................................................
- name: Import/create new repo with sample code
  uri:
    url: "{{ BITBUCKET_URL }}/rest/importer/latest/projects/{{ data.bb_project }}/import/repos"
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
          name: "{{ data.bb_repo }}"
          scmId: "git"
    body_format: json
    validate_certs: no
    status_code: [200, 201, 409]
  register: response

# .........................................................................
# 4. Grant necessary permissions to Bitbucket repo
# .........................................................................
- name: Construct permissions query string for REPO_ADMIN
  set_fact:
    admins_query: "permission=REPO_ADMIN{% for admin in data.bb_repo_admins %}&name={{ admin | urlencode}}{% endfor %}"
  when: data.bb_repo_admins is defined

- name: Grant necessary permissions to Bitbucket repo REPO_ADMIN
  uri:
    url: "{{ BITBUCKET_URL }}/rest/api/latest/projects/{{ data.bb_project }}/repos/{{ data.bb_repo }}/permissions/users?{{ admins_query }}"
    user: "{{ BITBUCKET_USER }}"
    password: "{{ BITBUCKET_PASS }}"
    force_basic_auth: yes
    headers:
      Content-Type: "application/json"
      Accept: "application/json"
    method: PUT
    validate_certs: no
    status_code: [200, 201, 204]
  register: response
  when: data.bb_repo_admins is defined
---
```

