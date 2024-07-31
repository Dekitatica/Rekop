import socket
import threading
import json
import sys
import time
import world
import utility
import pygame
pygame.init()

world_info = world.getworld()

# Money per second, cost
upgrades = {
    "1" : [5,30],
    "2" : [10,100],
    "3" : [20,850],
    "4" : [40,3500],
    "5" : [75,11000]
}


class Player:
    def __init__(self) -> None:
        self.money = 0
        self.x = 0
        self.y = 0
        self.w = 45
        self.h = 65
        self.id = "-1"
        self.team = "na"
        self.upgrades = {
            "1":False,
            "2":False,
            "3":False,
            "4":False,
            "5":False
        }
        self.multip = 1.00
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
            "miner_5" : -1
        }
    def toJSON(self):
        return super().toJSON()


def send_all_players(connections : list[Client]):
    players = []

    for cli in connections:
        players.append(cli.player.toJSON())


    json_obj = ("players%"+json.dumps(players)).encode()

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
            "atm_5" : -1
        }
    def toJSON(self):
        return super().toJSON()


def player_sender(connections):
    while True:
        try:
            send_all_players(connections)
            print(len(connections))
        except:
            pass
        time.sleep(1/60)


def request_move(cli : Client,args) -> None:
    global world_info
    speed = 5
    rect = pygame.Rect(cli.player.x,cli.player.y,cli.player.w,cli.player.h)


    keys = json.loads(args)
    zidovi = world_info["walls"]
    if keys["w"]:
        clear = 0
        for i in range(4):
            zid = zidovi[i]
            if pygame.Rect(rect.x,rect.y-speed,rect.width,rect.height).colliderect(zid) == False:
                clear+=1
        if clear==4:
            cli.player.y-=speed
            
        
    if keys["s"]:
        clear = 0
        for i in range(4):
            zid = zidovi[i]
            if pygame.Rect(rect.x, rect.y + speed , rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == 4:
            cli.player.y += speed
        
    if keys["d"]:
        clear = 0
        for i in range(4):
            zid = zidovi[i]
            if pygame.Rect(rect.x + speed , rect.y, rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == 4:

            cli.player.x += speed
        

    if keys["a"]:
        clear = 0
        for i in range(4):
            zid = zidovi[i]
            if pygame.Rect(rect.x -speed , rect.y , rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == 4:
            cli.player.x -= speed
    return


def send_world(cli : Client):
    global world_info
    world_info2 = {"walls":[]}
    for i in range(len(world_info["walls"])):
        world_info2["walls"].append(utility.rect_to_list(world_info["walls"][i]))  #Maybe have other stuff too?
    json_obj = json.dumps(world_info2)
    cli.con.sendall(("worlddata%"+json_obj).encode())

def earn_money_loop(clients : list[Client]):
    global upgrades 
    while True:
        for cli in clients:
            money_to_give = 0
            for up in cli.player.upgrades.keys():
                if cli.player.upgrades[up]:
                    money_to_give+=upgrades[up]
            cli.player.money+=money_to_give*cli.player.multip
        time.sleep(1)

def handle_client(cli : Client) -> None:
    global connections
    con = cli.con
    con.settimeout(3)
    while True:
        try:
            if cli.do_i_kill_myself:
                con.send("disconnect".encode()) # ah shit ovo je kad je not responding vrv nece ni primiti ovo
                del connections[connections.index(cli)]
                print("Client disconnect!")
                return
            data = con.recv(1024)
            data = data.decode()
            data = str(data)
            if data!="":
                cli.last_heartbeat_ms = 0
                if cli.player.team == "na":
                    if data.startswith("set_team%"):
                        args = data.split("%")[1]
                        if args=="bank":
                            cli.player.team="bank"
                        if args=="hero":
                            cli.player.team="hero"
                        
                
                elif data.startswith("heartbeat_received%"):
                    print("Beat received")
                    # Znam da je ovo vec uradjeno ali ovo je da bi se
                    # Razumeo kod
                    cli.last_heartbeat_ms = 0
                    continue
                if data.startswith("request_move%"):
                    request_move(cli,data.split("%")[1])
                print(data)
                

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                del connections[connections.index(cli)]
                return
            pass

available_ids = [1]*100

kicked = []

connections = []

#SERVER_HOST = '192.168.1.107'
SERVER_HOST = '127.0.0.1'
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
    newid = str(newid)
    new_client.player.id = newid
    send_world(new_client)
    new_client.con.sendall(f"id%{newid}".encode())


    connections.append(new_client)
    t1 = threading.Thread(target=handle_client(connections[-1]))
    t1.start()
    threads.append(t1)