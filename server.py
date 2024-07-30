import socket
import threading
import json
import sys
import time


class Player:
    def __init__(self) -> None:
        self.money = 0
        self.x = 0
        self.y = 0
        self.id = "-1"
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class Client:
    def __init__(self,player : Player,con : socket.socket) -> None:
        self.player = player
        self.con = con
        self.last_heartbeat_ms = round(time.time() * 1000)
        self.do_i_kill_myself = False



class Hero(Player):
    def __init__(self) -> None:
        super().__init__()
        self.upgrades = {
            "miner_1" : -1,
            "miner_2" : -1,
            "miner_3" : -1,
            "miner_4" : -1,
            "miner_5" : -1,
            "miner_6" : -1,
            "miner_7" : -1,
            "miner_8" : -1,
        }
    def toJSON(self):
        return super().toJSON()


class AntiHero(Player):
    def __init__(self) -> None:
        super().__init__()
        self.upgrades = {
            "atm_1" : -1,
            "atm_2" : -1,
            "atm_3" : -1,
            "atm_4" : -1,
            "atm_5" : -1,
            "atm_4" : -1,
            "atm_5" : -1,
        }
    def toJSON(self):
        return super().toJSON()


def client_kicker(connections):
    while True:

        time_in_ms = round(time.time() * 1000)
        for con in connections:
            if con.last_heartbeat_ms-time_in_ms>10000:
                #kick client logic

                con.do_i_kill_my_self = True
        time.sleep(1)


def request_move(cli,args) -> None:
    pass

def handle_client(cli : Client) -> None:
    con = cli.con
    con.settimeout(3)
    while True:
        try:
            if cli.do_i_kill_myself:
                con.send("disconnect".encode()) # ah shit ovo je kad je not responding vrv nece ni primiti ovo
                print("Client disconnect!")
                return
            data = con.recv(1024)
            data = data.decode()
            data = str(data)
            if data!="":
                print(data)
                cli.last_heartbeat_ms = 0
                if data.startswith("heartbeat_received:"):
                    print("Beat received")
                    # Znam da je ovo vec uradjeno ali ovo je da bi se
                    # Razumeo kod
                    cli.last_heartbeat_ms = 0
                if data.startswith("request_move:"):
                    request_move(data.split(":")[1])
                

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
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


#thread_client_kicker = threading.Thread(target=client_kicker,args=[connections])
#thread_client_kicker.start()

while True:
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    new_client = Client(Player(),client_socket)
    newid = -2
    for i in range(100):
        if available_ids[i]==1:
            newid = i
            available_ids[i] = 0
    new_client.player.id = newid



    connections.append(new_client)
    t1 = threading.Thread(target=handle_client(connections[-1]))
    t1.start()
    threads.append(t1)