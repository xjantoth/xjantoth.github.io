---
title: "Go NotFoundHandler()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to use http.NotFoundHandler in Go to return a 404 response for specific routes like favicon.ico."

tags: ['go']
categories: ["Go"]
---

This program demonstrates `http.NotFoundHandler()` in Go. The `NotFoundHandler` returns a handler that responds with a 404 Not Found status. It is commonly used to suppress browser requests for `/favicon.ico` that would otherwise be caught by the root `/` handler and clutter server logs.

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
