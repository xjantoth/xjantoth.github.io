---
title: "Go simple TCP server"
date: "2022-01-06T14:23:31+0100"
lastmod: "2022-01-06T14:23:31+0100"
draft: false
author: "Jan Toth"
image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=420&fit=crop"
description: "A minimal TCP echo server in Go that reads input from clients and echoes it back with a 10-second connection timeout."

tags: ['go', 'simple', 'tcp', 'server']
categories: ["Go"]
---

This example implements a minimal TCP echo server in Go. It listens on port 8080, accepts incoming connections, and for each connection reads input line by line using a `bufio.Scanner`. Each line received is echoed back to the client. The connection has a 10-second deadline after which it times out automatically.

```go
package main


import (
	"fmt"
	"time"
	"log"
	"net"
	"bufio"
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
	err := conn.SetDeadline(time.Now().Add(10 * time.Second))
	if err != nil {
		log.Println("Connection timeout!")
	}

	scanner := bufio.NewScanner(conn)

	for scanner.Scan() {
		ln := scanner.Text()
		fmt.Println(ln)
		fmt.Fprintf(conn, "I heard you say: %s\n", ln)
	}

	defer conn.Close()

	fmt.Println("Code got here.")
}
```
