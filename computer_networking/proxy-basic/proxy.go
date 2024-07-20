package main

import (
	"errors"
	"fmt"
	"io"
	"net"
	"syscall"
)

const (
	bufSize      = 4096
	upstreamAddr = "127.0.0.1:9000"
)

func main() {
	socket, err := net.Listen("tcp", "0.0.0.0:8090")
	if err != nil {
		panic(err)
	}

	for {
		clientConn, err := socket.Accept()
		if err != nil {
			panic(err)
		}

		go handleProxyConnection(clientConn)
	}
}

func handleProxyConnection(clientConn net.Conn) {
	fmt.Println("New connection accepted")
	upstreamConn, err := net.Dial("tcp", upstreamAddr)
	if err != nil {
		if errors.Is(err, syscall.ECONNREFUSED) {
			clientConn.Write([]byte("HTTP/1.1 502\r\n\r\n"))
			clientConn.Close()
			return
		}
	}

	for {
		buf := make([]byte, bufSize)
		readBytes, err := clientConn.Read(buf)

		if err != nil {
			if errors.Is(err, io.EOF) {
				upstreamConn.Close()
				clientConn.Close()
				return
			} else {
				panic(err)
			}
		}

		fmt.Printf("%s -> *: %dB\n", clientConn.LocalAddr().String(), readBytes)

		wroteBytes, err := upstreamConn.Write(buf[0:readBytes])
		if err != nil {
			panic(err)
		}
		fmt.Printf("* -> %s: %dB\n", upstreamConn.RemoteAddr().String(), wroteBytes)

		for {
			upstreamBuf := make([]byte, bufSize)
			readBytes, err := upstreamConn.Read(upstreamBuf)
			if err != nil {
				if errors.Is(err, io.EOF) {
					break // Listen for requests from client / jump to outer loop
				}
			}

			wroteBytes, err := clientConn.Write(upstreamBuf[0:readBytes])
			if err != nil {
				panic(err)
			}
			fmt.Printf("%s <- *: %dB\n", clientConn.RemoteAddr().String(), wroteBytes)
		}
	}
}
