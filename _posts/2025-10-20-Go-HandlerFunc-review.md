---
title: "Go HandlerFunc() review"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "A review of Go's http.HandlerFunc adapter, showing how to use it with http.Handle to register handler functions and render templates."

tags: ['go', 'review']
categories: ["Go"]
---

This example revisits `http.HandlerFunc` in Go. Instead of using `http.HandleFunc` (which accepts a plain function), this program wraps handler functions with `http.HandlerFunc(dogs)` and passes them to `http.Handle`. The handlers render HTML templates using `tpl.ExecuteTemplate`, demonstrating how to combine template rendering with the Handler interface pattern.

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
