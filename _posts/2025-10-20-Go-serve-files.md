---
title: "Go serve files"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go serve files"

tags: ['go', 'serve', 'files']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

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
