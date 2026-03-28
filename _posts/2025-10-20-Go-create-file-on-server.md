---
title: "Go create file on server"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to handle file uploads in Go by reading a multipart form file and saving it to the server filesystem."

tags: ['go', 'file', 'server']
categories: ["Go"]
---

This Go program implements a file upload server. When a user submits a file via a multipart form POST, the handler reads the uploaded file content, displays it in the browser, and saves a copy to the `user/` directory on the server. The template renders an upload form on GET and shows the file contents on POST.

```go

{% raw %}
package main

import (
	"fmt"
	"html/template"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
)

var tpl *template.Template

func init() {
	tpl = template.Must(template.ParseFiles("index.gohtml"))
}

func main() {
	http.HandleFunc("/", foo)
	http.Handle("/favicon.ico", http.NotFoundHandler())

	http.ListenAndServe(":8080", nil)
}

func foo(w http.ResponseWriter, r *http.Request) {
	var s string

	fmt.Printf("Request method: %v\n", r.Method)
	if r.Method == http.MethodPost {
		f, h, err := r.FormFile("q")

		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		defer f.Close()
		fmt.Printf("File: %v\n", f)
		fmt.Printf("Headers: %v\n", h)
		fmt.Printf("Error: %v\n", err)

		bs, err := ioutil.ReadAll(f)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		s = string(bs)

		// create a new file on the server
		// do not forget to create user/ folder manually at the server first
		newFile, err := os.Create(filepath.Join("user/", h.Filename+"_uploaded.txt"))
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		defer newFile.Close()

		_, err = newFile.Write(bs)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	tpl.ExecuteTemplate(w, "index.gohtml", s)

}


// Options for <form> and POST method in particular
// 	- <form method="POST" enctype="multipart/form-data">
// 	- <form method="POST" enctype="multipart/x-www-form-urlencoded">
// 	- <form method="POST" enctype="text/plain">


// cat index.gohtml
// <!DOCTYPE html>
// <html lang="en">
// <head>
//     <meta charset="UTF-8">
//     <title>Input Type Submit</title>
// </head>
// <body>


// <form method="POST" enctype="multipart/form-data">
//     <label for="idx-f">Choose File To Upload</label>
//     <input type="file" id="idx-f" name="q">
//     <br>
//     <input type="submit">
// </form>

// {{if .}}
// <h1>Here are the contents of the file:</h1>
// {{.}}
// {{end}}
// </body>
// </html>
{% endraw %}

```
