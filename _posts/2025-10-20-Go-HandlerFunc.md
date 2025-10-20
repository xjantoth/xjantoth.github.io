---
title: "Go HandlerFunc()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go HandlerFunc()"

tags: ['go']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

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
