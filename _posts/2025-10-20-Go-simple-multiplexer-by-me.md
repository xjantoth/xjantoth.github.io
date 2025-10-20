---
title: "Go simple multiplexer by me"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "/assets/images/blog/go-1.jpg"
description: "Go simple multiplexer by me"

tags: ['go', 'simple', 'multiplexer', 'by', 'me']
categories: ["tiddlywiki"]

hiddenFromSearch: false
---

```go
package main


import (
	"fmt"
	"log"
	"net"
	"bufio"
	"strings"
)

func main()  {
	li, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Panic(err)

	}

	defer li.Close()

	for {
		conn, err := li.Accept()
		if err != nil {
			log.Println(err)
		}

		go handle(conn)
	}
}

func handle(conn net.Conn)  {
	defer conn.Close()

	rURL := request(conn)
	response(conn, rURL)
}


func request(conn net.Conn) string {
	i := 0
	scanner := bufio.NewScanner(conn)
	var RequestURL string
	for scanner.Scan() {
		ln := scanner.Text()
		fmt.Println(ln)

		if i == 0 {
			m := strings.Fields(ln)[0]
			RequestURL = strings.Fields(ln)[1]
			fmt.Println("***METHOD:", m)
		}

		if ln == "" {
			// according RFC at the end of each request there
			// is the blank line and know this is really the END
			// so we "break" out of loop
			break
		}
		i++
	}
	return RequestURL
}

func returnedData(conn net.Conn, requestURL string, uniqText string)  {
	body := `<!DOCTYPE html>
	<html lang="en">
	<head><meta charset="UTF-8">
	<title></title>
	</head><body>
	<strong>` + uniqText + "Requested URL: " + requestURL +
	`</strong>
	</body>
	</html>`

	fmt.Fprint(conn, "HTTP/1.1 200 OK\r\n")
	fmt.Fprintf(conn, "Content-Length: %d\r\n", len(body))
	fmt.Fprint(conn, "Content-Type: text/html\r\n")

	fmt.Fprint(conn, "\r\n")
	fmt.Fprint(conn, body)
}

func response(conn net.Conn, requestURL string)  {
	switch {
	case requestURL == "/about":
			uniq := "ABOUT "
			returnedData(conn, requestURL, uniq)

	case requestURL == "/customers":
			uniq := "CUSTOMERS "
			returnedData(conn, requestURL, uniq)
	default:
			uniq := "EVERYTHING ELSE "
			returnedData(conn, requestURL, uniq)
	}


}
```
