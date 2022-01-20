import socket
sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = "127.0.0.1"
port = 8001
sct.bind((IP, port))
sct.listen(1)
print(f"Debug server is running {IP} on port {port}")

try:
    while True:
        clientsocket, address = sct.accept()
        data = clientsocket.recv(1024)
        print(data.decode('utf-8'))
        clientsocket.shutdown(socket.SHUT_WR)
except KeyboardInterrupt:
    print("Shutting down the server")
except Exception as exc:
    print("Debug server error: ", exc)
finally:
    sct.close()
