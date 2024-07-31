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
    "0" : [1,0],
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
            "0":True,
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




def send_all_players(connections : list[Client]):
    players = []

    for cli in connections:
        players.append(cli.player.toJSON())


    json_obj = ("players?"+json.dumps(players)).encode()

    for cli in connections:
        try:
            cli.con.sendall(json_obj)
        except Exception as e:
            print(e)

    pass



def player_sender(connections):
    while True:
        try:
            send_all_players(connections)
            #print(len(connections))
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
    cli.con.sendall(("worlddata?"+json_obj).encode())

def earn_money_loop(clients : list[Client]):
    global upgrades 
    while True:
        for cli in clients:
            money_to_give = 0
            for up in cli.player.upgrades.keys():
                if cli.player.upgrades[up]:
                    money_to_give+=upgrades[up][0]
            cli.player.money+=money_to_give*cli.player.multip
            print(f"[{cli.player.team.capitalize()}]: {cli.player.id} has {cli.player.money} coins!")
        time.sleep(1)

def buy_upgrade(cli : Client,upgrade_id):
    if cli.player.money >= upgrades[upgrade_id][1]:
        cli.player.money-= upgrades[upgrade_id][1]
        cli.player.upgrades[upgrade_id] = True



def handle_client(cli : Client) -> None:
    global connections
    con = cli.con
    con.settimeout(15)
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
                data2 = data.split("|")
                #print(data)
                for data in data2:
                    cli.last_heartbeat_ms = 0
                    if cli.player.team == "na":
                        if data.startswith("set_team?"):
                            args = data.split("?")[1]
                            if args=="bank":
                                cli.player.team="bank"
                            if args=="hero":
                                cli.player.team="hero"
                            
                    
                    elif data.startswith("heartbeat_received"):
                        print(f"{cli.player.id} Beat received")
                    if data.startswith("request_move?"):
                        request_move(cli,data.split("?")[1])
                    if data.startswith("buy_upgrade?"):
                        buy_upgrade(cli,data.split("?")[1])
                

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

thread_money_giver = threading.Thread(target=earn_money_loop,args=[connections])
thread_money_giver.start()

while True:
    print("start")
    server_socket.listen(10)
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
    connections.append(new_client)
    send_all_players(connections)
    time.sleep(0.2)
    new_client.con.sendall(f"id?{newid}".encode())
    time.sleep(0.2)
    send_world(new_client)
    


    print("pre-end")
    t1 = threading.Thread(target=handle_client,args=[connections[-1]])
    t1.start()
    threads.append(t1)
    print("end")