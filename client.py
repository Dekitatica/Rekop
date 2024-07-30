import threading
import sys
import socket
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 14242

def handle_server(client_socket):
    con = client_socket
    while True:
        try:
            data = con.recv(1024)
            data = data.decode()
            data = str(data)
            if data!="":
                print(data)
                if data.startswith("heartbeat:"):
                    beatid = data.split("")
                    client_socket.sendall(f"heartbeat_received:{beatid}".encode())

                

        except Exception as e:
            print(e)
            pass




client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

thread_server_handler = threading.Thread(target=handle_server,args=[client_socket])

while True:
    pass