import socket
import threading
import json
import sys
import time
import random


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

class Team:
    def __init__(self,id) -> None:
        self.money = 0
        self.name = id
        self.members = []
        self.multip = 1.00
        self.latest_upgrade = "0"
        self.upgrades = {
            "0" : True,
            "1" : False,
            "2" : False,
            "3" : False,
            "4" : False,
            "5" : False
        }
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)


team_bank = Team("bank")
team_hero = Team("hero")

teams = {
    "bank" : team_bank,
    "hero" : team_hero
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
        self.blj_active = False
        self.blj_feed = []
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
        self.do_i_kill_myself = False # Terminate thread when sent to True




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
            time.sleep(1/60)
            send_all_teams(connections)
            #print(len(connections))
        except Exception as e:
            print(e)
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
        for i in range(len(zidovi)):
            zid = zidovi[i]
            if pygame.Rect(rect.x,rect.y-speed,rect.width,rect.height).colliderect(zid) == False:
                clear+=1
        if clear==len(zidovi):
            cli.player.y-=speed
            
        
    if keys["s"]:
        clear = 0
        for i in range(len(zidovi)):
            zid = zidovi[i]
            if pygame.Rect(rect.x, rect.y + speed , rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == len(zidovi):
            cli.player.y += speed
        
    if keys["d"]:
        clear = 0
        for i in range(len(zidovi)):
            zid = zidovi[i]
            if pygame.Rect(rect.x + speed , rect.y, rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == len(zidovi):

            cli.player.x += speed
        

    if keys["a"]:
        clear = 0
        for i in range(len(zidovi)):
            zid = zidovi[i]
            if pygame.Rect(rect.x -speed , rect.y , rect.width , rect.height).colliderect(zid) == False:
                clear +=1
        if clear == len(zidovi):
            cli.player.x -= speed
    return


def send_world(cli : Client):
    global world_info
    world_info2 = {"walls":[]}
    for i in range(len(world_info["walls"])):
        world_info2["walls"].append(utility.rect_to_list(world_info["walls"][i]))  #Maybe have other stuff too?
    json_obj = json.dumps(world_info2)
    cli.con.sendall(("worlddata?"+json_obj).encode())

teams = [team_hero,team_bank]
teams_dict = {
    "bank":team_bank,
    "hero":team_hero
}
def earn_money_loop(teams : list[Client]):
    global upgrades 
    while True:
        if len(team_bank.members) != 0 and len(team_hero.members)!=0:
            for team in teams:
                money_to_give = 0
                for up in team.upgrades.keys():
                    if team.upgrades[up]:
                        money_to_give+=upgrades[up][0]
                team.money+=money_to_give*team.multip
                print(f"[{team.name.capitalize()}]: {team.money} coins!")
                if team.money >= 15000:
                    print("You win!")
                    for cli in teams:
                        if cli.player.team == team:
                            cli.con.sendall("end?You win!".encode())
                        else:
                            cli.con.sendall("emd?L".encode())
        time.sleep(1)

def buy_upgrade(cli : Client):
    upgrade_id = "-1"
    for key in teams_dict[cli.player.team].upgrades:
        if teams_dict[cli.player.team].upgrades[key] == False:
            upgrade_id = key
            break
    if teams_dict[cli.player.team].money >= upgrades[upgrade_id][1] and teams_dict[cli.player.team].upgrades[upgrade_id] == False and upgrade_id!="-1":
        teams_dict[cli.player.team].money-= upgrades[upgrade_id][1]
        teams_dict[cli.player.team].upgrades[upgrade_id] = True
        teams_dict[cli.player.team].latest_upgrade = upgrade_id

def send_all_teams(clients : list[Client]):
    teams_dict2 = {}
    for key in teams_dict.keys():
        teams_dict2[key] = teams_dict[key].toJSON()

    json_obj = json.dumps(teams_dict2)
    for cli in clients:
        cli.con.sendall(f"teams?{json_obj}".encode())

def blj(cli : Client,bet : int):
    available_cards = []
    player_cards = []
    for i in range(2,14):
        for j in range(4):
            available_cards.append(min(i,10))
    dealer = [utility.pick_a_card(available_cards,[])]
    dealer.append(utility.pick_a_card(available_cards,dealer))

    player_cards.append(utility.pick_a_card(available_cards,player_cards))

    cli.con.sendall(f"dealer_cards?{json.dumps(dealer[1:len(dealer)])}")
    cli.con.sendall(f"your_cards?{json.dumps(player_cards)}")
    extra_wager = -1
    while True:
        if len(cli.player.blj_feed)!=0:
            com = str(cli.player.blj_feed[0])
            if com.startswith("blj_hit?"):
                player_cards.append(utility.pick_a_card(available_cards,player_cards))
                cli.con.sendall(f"your_cards?{json.dumps(player_cards)}")

                if sum(player_cards)>21:
                    cli.con.sendall(f"blj_end?loss;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                    cli.player.money-=bet
                    return
            if com.startswith("blj_stand?"):
                while True:
                    if sum(dealer)<17:
                        dealer.append(utility.pick_a_card(available_cards,dealer))
                        cli.con.sendall(f"dealer_cards?{json.dumps(dealer[1:len(dealer)])}")
                        if sum(dealer)>21:
                            cli.con.sendall(f"blj_end?win;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money+=bet
                            return
                    else:
                        if sum(player_cards)>sum(dealer):
                            cli.con.sendall(f"blj_end?win;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money+=bet
                            return
                        else:
                            cli.con.sendall(f"blj_end?loss;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money-=bet
                            return
            if com.startswith("blj_double_down?") and extra_wager!=-1:
                player_cards.append(utility.pick_a_card(available_cards,player_cards))
                cli.con.sendall(f"your_cards?{json.dumps(player_cards)}")
                if sum(player_cards)>21:
                    cli.con.sendall(f"blj_end?loss;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                    cli.player.money-=bet
                    return          
                while True:
                    if sum(dealer)<17:
                        dealer.append(utility.pick_a_card(available_cards,dealer))
                        cli.con.sendall(f"dealer_cards?{json.dumps(dealer[1:len(dealer)])}")
                        if sum(dealer)>21:
                            cli.con.sendall(f"blj_end?win;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money+=bet
                            return
                    else:
                        if sum(player_cards)>sum(dealer):
                            cli.con.sendall(f"blj_end?win;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money+=bet
                            return
                        else:
                            cli.con.sendall(f"blj_end?loss;{json.dumps(player_cards)};{json.dumps(dealer)};{bet}")
                            cli.player.money-=bet
                            return                       

            pass
        pass




def handle_client(cli : Client) -> None:
    global connections
    con = cli.con
    con.settimeout(15)
    while True:
        try:
            if cli.do_i_kill_myself:
                con.send("disconnect".encode())
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
                                if cli.player.id not in team_bank.members:
                                    team_bank.members.append(cli.player.id)
                                    cli.player.x = 600
                                    cli.player.y = 400
                            if args=="hero":
                                cli.player.team="hero"
                                if cli.player.id not in team_hero.members:
                                    team_hero.members.append(cli.player.id)
                                    cli.player.x = 100
                                    cli.player.y = 100
                    
                    elif data.startswith("heartbeat_received"):
                        print(f"{cli.player.id} Beat received")
                    if data.startswith("request_move?"):
                        request_move(cli,data.split("?")[1])
                    if data.startswith("buy_upgrade?"):
                        buy_upgrade(cli)
                    if data.startswith("teleport_to_bank?"):
                        cli.player.x = 42200    
                        cli.player.y = 200
                    if data.startswith("coinflip?"):
                        args = int(data.split("?")[1])
                        if teams_dict[cli.player.team].money>=args:
                            rint = random.randint(0,100)
                            if rint>=37:
                                teams_dict[cli.player.team].money+=args
                            else:
                                teams_dict[cli.player.team].money-=args
                    if data.startswith("blj?"):
                        bet = data.split("?")[1]
                        bet = int(bet)
                        if bet<=cli.player.money:
                            cli.player.blj_active = True
                            blj(cli,bet)
                    if cli.player.blj_active and data.startswith("blj_hit?"):
                        cli.player.blj_feed.append(data)
                        pass


        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e) or "Broken pipe" in str(e):
                del connections[connections.index(cli)]
                return
            pass

if __name__=="__main__":

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

    thread_money_giver = threading.Thread(target=earn_money_loop,args=[teams])
    thread_money_giver.start()

    while True:
        print("start")
        server_socket.listen(10)
        print(f"[*] Listening on {SERVER_HOST}:{SERVER_PORT}")

        client_socket, client_address = server_socket.accept()
        print(f"[*] Accepted connection from {client_address[0]}:{client_address[1]}")
        
        new_client = Client(Player(),client_socket)
        new_client.player.x = -100
        new_client.player.y = -100
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