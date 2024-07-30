import socket
import threading
import json
import sys
import time
import world
import utility


world_info = world.getworld()

class Player:
    def __init__(self) -> None:
        self.money = 0
        self.x = 0
        self.y = 0
        self.id = "-1"
        self.team = "na"
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


def send_all_players(connections : list[Client]):
    players = []

    for cli in connections:
        cli.player.money+=1
        players.append(cli.player.toJSON())


    json_obj = ("players:"+json.dumps(players)).encode()

    for cli in connections:
        try:
            cli.con.sendall(json_obj)
        except Exception as e:
            print(e)

    pass


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


def player_sender(connections):
    while True:
        try:
            send_all_players(connections)
            print("sentt")
        except:
            pass
        time.sleep(1)


def request_move(cli,args) -> None:

    pass


def send_world(cli : Client):
    for i in range(len(world_info["walls"])):
        world_info["walls"][i] = utility.rect_to_list(world_info["walls"][i])
    json_obj = json.dumps(world_info)
    cli.con.sendall(json_obj.encode())


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
                cli.last_heartbeat_ms = 0
                if cli.player.team == "na":
                    if data.startswith("set_team:"):
                        args = data.split(":")[1]
                        if args=="bank":
                            cli.player.team="bank"
                        if args=="hero":
                            cli.player.team="hero"
                        
                
                elif data.startswith("heartbeat_received:"):
                    print("Beat received")
                    # Znam da je ovo vec uradjeno ali ovo je da bi se
                    # Razumeo kod
                    cli.last_heartbeat_ms = 0
                    continue
                if data.startswith("request_move:"):
                    request_move(data.split(":")[1])
                print(data)
                

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
            pass

available_ids = [1]*100

kicked = []

connections = []

SERVER_HOST = '192.168.1.107'
#SERVER_HOST = '127.0.0.1'
SERVER_PORT = 14242

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((SERVER_HOST, SERVER_PORT))

threads = []


thread_client_kicker = threading.Thread(target=player_sender,args=[connections])
thread_client_kicker.start()

while True:
    server_socket.listen(5)
    print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")

    new_client = Client(Player(),client_socket)
    new_client.player.x = 100
    new_client.player.y = 100
    newid = -2
    for i in range(100):
        if available_ids[i]==1:
            newid = i
            available_ids[i] = 0
            break
    new_client.player.id = newid



    connections.append(new_client)
    t1 = threading.Thread(target=handle_client(connections[-1]))
    t1.start()
    threads.append(t1)