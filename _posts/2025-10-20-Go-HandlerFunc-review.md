---
title: "Go HandlerFunc() review"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go HandlerFunc() review"

tags: ['go', 'handlerfunc()', 'review']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"html/template"
	"net/http"
)

var tpl *template.Template

func init() {
	tpl = template.Must(template.ParseFiles("index.gohtml"))
}

func dogs(w http.ResponseWriter, r *http.Request) {
	// io.WriteString(w, "This is the web about dogs!\n")
	data := `This is the web about dogs!\n`
	w.Header().Set("Content-type", "text/html")
	tpl.ExecuteTemplate(w, "index.gohtml", data)
}

func me(w http.ResponseWriter, r *http.Request) {
	// io.WriteString(w, "This is the web about me!\n")
	data := `This is the web about me!\n`
	tpl.ExecuteTemplate(w, "index.gohtml", data)
}

func about(w http.ResponseWriter, r *http.Request) {
	// io.WriteString(w, "About!\n")
	data := `About me!\n`
	tpl.ExecuteTemplate(w, "index.gohtml", data)
}

func main() {

	// http.HandleFunc("/dogs/", dogs)
	// http.HandleFunc("/me/", me)
	// http.HandleFunc("/", about)
	http.Handle("/dogs/", http.HandlerFunc(dogs))
	http.Handle("/me/", http.HandlerFunc(me))
	http.Handle("/", http.HandlerFunc(about))


	http.ListenAndServe(":8080", nil)

}

```
