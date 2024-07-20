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

	for {
		upstreamConn, err := net.Dial("tcp", upstreamAddr)

		if err != nil {
			if errors.Is(err, syscall.ECONNREFUSED) {
				clientConn.Write([]byte("HTTP/1.1 502\r\n\r\n"))
				clientConn.Close()
				return
			}
		}

		clientBuf := make([]byte, bufSize)
		readBytes, err := clientConn.Read(clientBuf)
		if err != nil {
			if errors.Is(err, io.EOF) {
				fmt.Println("EOF on client")
				break
			} else {
				panic(err)
			}
		}
		fmt.Printf("%s -> *: %dB\n", clientConn.LocalAddr().String(), readBytes)

		wroteBytes, err := upstreamConn.Write(clientBuf[0:readBytes])
		if err != nil {
			panic(err)
		}

		fmt.Printf("* -> %s: %dB\n", upstreamConn.RemoteAddr().String(), wroteBytes)

		for {
			upstreamBuf := make([]byte, bufSize)
			upstreamReadBytes, err := upstreamConn.Read(upstreamBuf)
			if err != nil {
				if errors.Is(err, io.EOF) { // All data from upstream socket is read, continue
					fmt.Println("EOF on upstream")
					fmt.Printf("len of upstream buf: %d\n", len(upstreamBuf))
					break
				} else {
					panic(err)
				}
			}
			fmt.Printf("* <- %s: %dB\n", upstreamConn.RemoteAddr().String(), upstreamReadBytes)

			upstreamWroteBytes, err := clientConn.Write(upstreamBuf[0:upstreamReadBytes])
			if err != nil {
				panic(err)
			}
			fmt.Printf("%s <- *: %dB\n", clientConn.RemoteAddr().String(), upstreamWroteBytes)
		}
	}

	fmt.Println("Closing connection")
	clientConn.Close()
}
