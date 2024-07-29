import socket
import threading

def handle_client(con):
    while True:
        try:
            data = con.recv(1024)
            data = data.decode()
            if data!="":
                print(data)
        except Exception as e:
            pass

available_ids = [1]*100

kicked = []

connections = []


SERVER_HOST = '10.68.21.27'
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 14242

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))

threads = []

while True:
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    connections.append(client_socket)
    t1 = threading.Thread(target=handle_client(connections[-1]))
    t1.start()
    threads.append(t1)