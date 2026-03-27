---
title: "Go NotFoundHandler()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go NotFoundHandler() with working code examples."

tags: ['go']
categories: ["Go"]
---

```go
package main

import (
	"fmt"
	"io"
	"net/http"
)

func main() {

	http.HandleFunc("/", index)

	http.Handle("/favicon.ico", http.NotFoundHandler())
	http.ListenAndServe(":8080", nil)
}

func index(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("requested url: %v\n", r.URL)
	io.WriteString(w, "Hello from Go dude!")
}

```
