---
title: "Go upload file"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go upload file with working code examples."

tags: ['go', 'file']
categories: ["Go"]
---

```go
package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
)

func main() {
	http.HandleFunc("/", foo)
	http.Handle("/favicon.ico", http.NotFoundHandler())

	http.ListenAndServe(":8080", nil)
}

func foo(w http.ResponseWriter, r *http.Request) {
	var s string

	fmt.Printf("Request method: %v\n", r.Method)
	if r.Method == http.MethodPost {
		f, h, err := r.FormFile("q")

		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		defer f.Close()
		fmt.Printf("File: %v\n", f)
		fmt.Printf("Headers: %v\n", h)
		fmt.Printf("Error: %v\n", err)

		bs, err := ioutil.ReadAll(f)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		s = string(bs)
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, `
	<form method="POST" enctype="multipart/form-data">
	<input type="file" name="q">
	<input type="submit">
	</form>
	` + s)

}

```
