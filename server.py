import socket
import threading
import json
import sys



class Player:
    def __init__(self) -> None:
        self.money = 0
        self.x = 0
        self.y = 0
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

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

class Client:
    def __init__(self,player : Player,con : socket.socket) -> None:
        self.player = player
        self.con = con

def request_move(cli,args) -> None:
    pass

def handle_client(cli : Client) -> None:
    con = cli.con
    while True:
        try:
            data = con.recv(1024)
            data = data.decode()
            data = str(data)
            if data!="":
                print(data)
                if data.startswith("request_move"):
                    request_move(data.split(":")[1])
                

        except Exception as e:
            print(e)
            pass

available_ids = [1]*100

kicked = []

connections = []

pl = Player()
ah = AntiHero()
he = Hero()

objs = [pl,ah,he]

for i in range(3):
    f = open(f"file_{i}.json","w")
    f.write(objs[i].toJSON())
    f.close()


exit()
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

    new_client = Client(Player(),client_socket)


    connections.append(new_client)
    t1 = threading.Thread(target=handle_client(connections[-1]))
    t1.start()
    threads.append(t1)