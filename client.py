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

                

        except Exception as e:
            print(e)
            pass



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

