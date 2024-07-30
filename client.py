

import threading
import sys
import socket
import json
from Player import Player

def dictToPlayer(d):
    p1 = Player(d["x"],d["y"],d["id"],d["money"])
    p1.team = d["team"]
    return p1
#haha

def handle_server(client_socket):
    global players
    con = client_socket
    while True:
        try:
            data = con.recv(4096)
            data = data.decode()
            data = str(data)
            if data!="":
                print(data)
                if data.startswith("heartbeat:"):
                    beatid = data.split("")[1]
                    client_socket.sendall(f"heartbeat_received:{beatid}".encode())
                if data.startswith("players:"):
                    dat = data.split("players:")[1]
                    players = json.loads(dat)
                    for i in range(len(players)):
                        players[i] = dictToPlayer(json.loads(players[i]))

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
            pass


SERVER_HOST = '127.0.0.1'
SERVER_PORT = 14242
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))


thread_server_handler = threading.Thread(target=handle_server,args=[client_socket])
thread_server_handler.start()
frame_count = 0

players = []

client_socket.sendall("set_team:bank".encode())
while True:
    if frame_count%1000==0:
        try:
            client_socket.sendall("heartbeat_received".encode())
        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                break
            pass


    frame_count+=1
    pass
