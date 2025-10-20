---
title: "Go serving files hands on 1"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go serving files hands on 1"

tags: ['go', 'serving', 'files', 'hands', 'on']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"html/template"
	"io"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", foo)
	http.HandleFunc("/dog/", dog)
	http.HandleFunc("/dog.jpg", chien)

	log.Fatalln(http.ListenAndServe(":8080", nil))

}

func foo(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "foo.run")
}

func dog(w http.ResponseWriter, r *http.Request) {
	tpl, err := template.ParseFiles("dog.gohtml")
	if err != nil {
		log.Fatalln(err)
	}
	tpl.ExecuteTemplate(w, "dog.gohtml", nil)
}

func chien(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "tesla.jpg")
}

```
