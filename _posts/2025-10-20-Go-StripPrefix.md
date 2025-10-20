---
title: "Go StripPrefix()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go StripPrefix()"

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

func main() {
	http.Handle("/resources/", http.StripPrefix("/resources", http.FileServer(http.Dir("./assets"))))

	http.HandleFunc("/xyz", takeAdvantageOfStripPrefix)

	http.HandleFunc("/tesla", teslaFromFileSystem)
	http.ListenAndServe(":8080", nil)

}

func teslaFromFileSystem(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, `<img src="tesla.jpg">`)
}

func takeAdvantageOfStripPrefix(w http.ResponseWriter, r *http.Request)  {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, `<img src="/resources/tesla.jpg">`)
}



```
