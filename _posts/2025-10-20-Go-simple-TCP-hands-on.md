---
title: "Go simple TCP hands on"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go simple TCP hands on"

tags: ['go', 'simple', 'tcp', 'hands', 'on']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"time"
	"strings"
)

func main() {
	li, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalln(err)
	}

	defer li.Close()

	for {
		conn, err := li.Accept()
		if err != nil {
			log.Fatalln(err)
		}
		go serve(conn)
	}

}

func serve(conn net.Conn) {
	err := conn.SetDeadline(time.Now().Add(30 * time.Second))
	if err != nil {
		log.Println(err)
	}

	scanner := bufio.NewScanner(conn)

	del := `[---------------]`
	fmt.Printf("Received: %v\n\n", del)

	i := 0

	// the following loop works in a way:
	// 1. run: curl -H "X-Head:Jao" -X POST http://127.0.0.1:8080/aaa
	// 2. curl sends:
	//           index: [0]: POST /aaaaaaaa HTTP/1.1
	//           index: [1]: Host: 127.0.0.1:8080
	//           index: [2]: User-Agent: curl/7.72.0
	//           index: [3]: Accept: */*
	// 			 index: [4]: X-Content-type:Jano
	// 			 index:	[5]:
	// 3. scanner.Scan() scans this 6 lines
	// 4. and prints them: periodically
	// 5. after an empty line => we write body variable :)

	var method string
	var path string

	for scanner.Scan() {
		ln := scanner.Text()
		// what I received as a server from a client
		fmt.Printf("[%v]: %v\n", i, ln)

		// how I am going to respond to client
		// io.WriteString(conn, "I the server say: Hello!\n - " + ln)
		// fmt.Printf("\n\n%v\n\n", del)

		if i == 0 {
			splitOnSpace := strings.Fields(ln)
			method = splitOnSpace[0]
			path = splitOnSpace[1]
		}
		if ln == "" {
			fmt.Println("THIS IS THE END :)")
			break
		}
		i++
	}
	body := response(method, path)

	fmt.Fprintf(conn, "HTTP/1.1 200 OK\r\n")
	fmt.Fprintf(conn, "Content-Type: text/html\r\n")
	fmt.Fprintf(conn, "Content-Length: %d\r\n", len(body))
	fmt.Fprintf(conn, "\r\n")
	fmt.Fprintf(conn, body)
	fmt.Printf("END: %v\n\n", del)

	defer conn.Close()

	// io.WriteString(conn, "I can see you connected")
}

func response(m string, url string) string {
	body := `
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>Input Type Submit</title>
	</head>
	<body>

	<h1>Hello from GO!
	` + "Method: " + m + " Requested URL: " + url + `
	</h1>

	</body>
	</html>
`
	return body
}

```
