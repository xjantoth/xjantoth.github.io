---
title: "Go serve files"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to serve static files in Go using http.ServeFile, io.Copy, and http.ServeContent, with examples for serving images from the local filesystem and the internet."

tags: ['go', 'serve', 'files']
categories: ["Go"]
---

This example demonstrates three different ways to serve files in Go: using `io.Copy`, `http.ServeContent`, and `http.ServeFile`. The server registers handlers for the root path (which renders an HTML image tag), a direct image route, and a route that serves an image referenced from the internet.

```go
package main

import (
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/frominternets", fromInternet)
	http.HandleFunc("/", teslaAsReference)
	http.HandleFunc("/tesla.jpg", tesla)
	http.ListenAndServe(":8080", nil)

}

func teslaAsReference(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	io.WriteString(w, `<img src="/tesla.jpg">`)
}

func tesla(w http.ResponseWriter, r *http.Request) {
	f, err := os.Open("tesla.jpg")
	if err != nil {
		log.Fatalln(err)
	}

	defer f.Close()
	// w.Header().Set("Contnt-Type", "text/html; charset=utf-8")
	// io.WriteString(w, `<h1>This is being served from io.Copy(w, f)!</h1>`)

	// 1. way: io.Copy(w, f)
	// io.Copy(w, f)

	// 2. way: http.ServeContent(w, r, infoImage.Name(), infoImage.ModTime(), f)
	// infoImage, err := f.Stat()
	// if err != nil {
	// 	http.Error(w, "file not found", 404)
	// 	return
	// }
	// http.ServeContent(w, r, infoImage.Name(), infoImage.ModTime(), f)

	// 3. way: http.ServeFile(w, r, "tesla.jpg")
	http.ServeFile(w, r, "tesla.jpg")


}

func fromInternet(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Contnt-Type", "text/html; charset=utf-8")
	io.WriteString(w, `<h1>This is being served from internet!</h1>`)
	io.WriteString(w, `
	<!-- not serving from our server-->
	<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/2018_Tesla_Model_S_75D.jpg/800px-2018_Tesla_Model_S_75D.jpg">`)

}

```
