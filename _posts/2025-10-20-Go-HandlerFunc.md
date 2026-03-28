---
title: "Go HandlerFunc()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to use http.HandlerFunc in Go to convert regular functions into HTTP handlers and register them with http.Handle."

tags: ['go']
categories: ["Go"]
---

This program demonstrates Go's `http.HandlerFunc` type adapter. The `http.HandlerFunc` function converts a regular function with the `(http.ResponseWriter, *http.Request)` signature into a type that satisfies the `http.Handler` interface, allowing it to be passed to `http.Handle`. This is useful when you want to use the `Handle` method instead of `HandleFunc`.

```go
package main

import (
	"io"
	"net/http"
)


func dogs(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "This is the web about dogs!\n")
}


func cats(w http.ResponseWriter, r *http.Request)  {
	io.WriteString(w, "This is the web about cats!\n")
}

func main() {

	http.Handle("/dogs/", http.HandlerFunc(dogs))
	http.Handle("/cats",  http.HandlerFunc(cats))

	http.ListenAndServe(":8080", nil)

}

```
