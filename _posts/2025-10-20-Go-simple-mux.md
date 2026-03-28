---
title: "Go simple mux"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "Implementing a simple multiplexer in Go by defining a custom type that satisfies the http.Handler interface with ServeHTTP."

tags: ['go', 'simple', 'mux']
categories: ["Go"]
---

This example shows how to create a simple multiplexer in Go by defining a custom type (`pes`) that implements the `http.Handler` interface via the `ServeHTTP` method. The handler parses the request URL path and routes to different responses using a switch statement. This custom handler is passed directly to `http.ListenAndServe` instead of using the default `ServeMux`.

```go
package main

import (
	"io"
	// "html/template"
	"log"
	"net/http"
	// "net/url"
)

// var tpl *template.Template

// func init() {
// 	tpl = template.Must(template.ParseFiles("index.gohtml"))
// }

type pes int

func (p pes) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	err := r.ParseForm()
	if err != nil {
		log.Fatalln(err)
	}

	// data := struct {
	// 	Method         string
	// 	URL            *url.URL
	// 	Submissions    map[string][]string
	// 	Header         http.Header
	// 	Host           string
	// 	ContentLength  int64
	// }{
	// 	Method: r.Method,
	// 	URL: r.URL,
	// 	Submissions: r.Form,
	// 	Header: r.Header,
	// 	Host: r.Host,
	// 	ContentLength: r.ContentLength,
	// }

	// for k, v := range r.Header {
	// 	fmt.Printf("[%v]: %v\n", k, v)
	// }

	// fmt.Println()

	// for k, v := range r.Form {
	// 	fmt.Printf("Form data: [%v]: %v\n", k, v)
	// }

	// w.Header().Set("X-Custom-Header", "this is go")
	// tpl.ExecuteTemplate(w, "index.gohtml", data)

	switch r.URL.Path {
	case "/dog":
		io.WriteString(w, "this is \"/dog\" path")
	case "/cat":
		io.WriteString(w, "this is \"/cat\" path")
	default:
		io.WriteString(w, "No matching /path")

	}


}

func main() {
	var styriPesa pes
	http.ListenAndServe(":8080", styriPesa)
}

```
