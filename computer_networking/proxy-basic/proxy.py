import socket

PROXY_ADDR = ('0.0.0.0', 8090)
UPSTREAM_ADDR = ('127.0.0.1', 9000)

if __name__ == "__main__":
    p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    p_socket.bind(PROXY_ADDR)
    p_socket.listen(10)
    print(f'"Listening for connections on {PROXY_ADDR}')

    while True:
        try:
            client_socket, client_addr = p_socket.accept()
            client_bytes = client_socket.recv(1050)
            print(f'{client_addr} -> *: {len(client_bytes)}B')

            upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            upstream_socket.connect(UPSTREAM_ADDR)
            upstream_socket.send(client_bytes)
            print(f'* -> {UPSTREAM_ADDR}: {len(client_bytes)}B')

            while True:
                upstream_bytes = upstream_socket.recv(1050)
                print(f'* <- {UPSTREAM_ADDR}: {len(upstream_bytes)} bytes')

                if len(upstream_bytes) == 0:
                    break

                client_socket.send(upstream_bytes)
                print(f'{client_addr} <- *: {len(upstream_bytes)} bytes')
        except KeyboardInterrupt:
            print("Interrupting..")
            exit(0)
        except ConnectionRefusedError:
            client_socket.send(b'HTTP/1.1 502\r\n\r\n')
        finally:
            upstream_socket.close()
            client_socket.close()