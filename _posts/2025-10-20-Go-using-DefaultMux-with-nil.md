---
title: "Go using DefaultMux with nil"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go using DefaultMux with nil with working code examples."

tags: ['go', 'using', 'defaultmux', 'nil']
categories: ["Go"]
---

```go
package main

import (
	"io"
	"net/http"
)

type pageDog int

func (pd pageDog) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "This is the web about dogs!\n")
}

type pageCat []string

func (pc pageCat) ServeHTTP(w http.ResponseWriter, r *http.Request)  {
	io.WriteString(w, "This is the web about cats!\n")
}

func main() {

	var dogs pageDog
	var cats pageCat

	http.Handle("/dogs/", dogs)
	http.Handle("/cats", cats)

	http.ListenAndServe(":8080", nil)

}

```
