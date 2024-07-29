import threading
import sys
import socket
import json

SERVER_HOST = '10.68.21.27'
SERVER_PORT = 14242

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_socket.sendall("Cao".encode())