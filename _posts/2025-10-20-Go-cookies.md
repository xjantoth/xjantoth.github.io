---
title: "Go cookies"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "How to set, read, and expire HTTP cookies in a Go web server using the net/http package."

tags: ['go', 'cookies']
categories: ["Go"]
---

This Go program demonstrates full cookie lifecycle management in an HTTP server. It provides routes to set multiple cookies (including a visit counter), read all cookies from the request, and expire a specific cookie by setting its `MaxAge` to -1. The server uses `http.SetCookie` to write cookies and `r.Cookies()` to read them back.

```go
package main

import (
	"fmt"
	"io"
	"net/http"
	"strconv"
)

func main() {
	http.HandleFunc("/", index)
	http.HandleFunc("/set", setCookie)
	http.HandleFunc("/read", readCookie)
	http.HandleFunc("/expire", expireCookie)
	http.Handle("/favicon.ico", http.NotFoundHandler())
	http.ListenAndServe(":8080", nil)

}


func index(w http.ResponseWriter, r *http.Request)  {
	fmt.Fprintln(w, `<h1><a href="/set">set a cookie</a><h1>`)
}

var visits int = 0 // How many times the client visited server

func setCookie(w http.ResponseWriter, r *http.Request) {

	visits++
	tmpVisits := strconv.Itoa(visits)
	w.Header().Set("Content-Type", "text/html")

	http.SetCookie(w, &http.Cookie{
		Name:  "my-cookie-from-golang-course",
		Value: "27",
	})

	http.SetCookie(w, &http.Cookie{
		Name:  "other-cookies",
		Value: "2",
	})

	http.SetCookie(w, &http.Cookie{
		Name:  "visited-cookies",
		Value: tmpVisits,
	})
	fmt.Fprintln(w, `<p>Cookie written - check your browser</p><br><h1><a href="/read">read</a><h1>`)
}

func readCookie(w http.ResponseWriter, r *http.Request) {
	// c, err := r.Cookie("my-cookie-from-golang-course")
	// if err != nil {
	// 	http.Error(w, err.Error(), http.StatusNotFound)
	// 	return
	// }
	// fmt.Fprintln(w, "Your cookie: ", c)

	// Read all cookies
	w.Header().Set("Content-Type", "text/html")
	sliceOfCookie := r.Cookies()

	if len(sliceOfCookie) != 0 {
		for idx, i := range sliceOfCookie {
			fmt.Fprintf(w, "[%v]: %v\n", idx, i)

		}
		io.WriteString(w, `<h1><h1><a href="/expire">expire</a></h1>`)
	} else {
		fmt.Fprintln(w, `<h1>
		There is no cookie whatsoever!
		<a href="/read">read</a><h1>`)
	}



}

func expireCookie(w http.ResponseWriter, r *http.Request)  {
	c, err := r.Cookie("visited-cookies")
	if err != nil {
		http.Redirect(w, r, "/set", http.StatusSeeOther)
		return
	}

	c.MaxAge = -1 // deletes the cookies
	http.SetCookie(w, c)
	http.Redirect(w, r, "/", http.StatusSeeOther)
}
```
