---
title: "Go request.FormValue('xyz')"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Go programming: Go request.FormValue('xyz') with working code examples."

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
	user := r.FormValue("user")
	surname := r.FormValue("surname")
	w.Header().Set("Content-type", "text/html")

	fmt.Printf("requested url: %v\n", r.URL)
	fmt.Printf("input variable user: %v\n", user)
	// io.WriteString(w, "Hello from Go dude! Username: " + v + "\n")

	io.WriteString(w, `
	<p>Now the form requires POST (user)</p>
	<form method="post">
		<input type="text" name="user">
		<input type="submit">
	</form>
	` + user + `<p>Now the form requires GET (surname)</p>
	<form method="get">
	<input type="text" name="surname">
	<input type="submit">
	</form>` + surname)
}

```
