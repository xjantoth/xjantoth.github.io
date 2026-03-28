---
title: "Go StripPrefix()"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Using http.StripPrefix in Go to serve static files from a local assets directory through a custom URL prefix."

tags: ['go']
categories: ["Go"]
---

This example shows how `http.StripPrefix` works with `http.FileServer` to serve static files. Requests to `/resources/` have the prefix stripped and are then served from the `./assets` directory. The `/xyz` handler demonstrates referencing these assets from an HTML response, while the `/tesla` handler attempts to serve a file without StripPrefix for comparison.

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
