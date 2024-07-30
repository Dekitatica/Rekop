import threading
import sys
import socket
import json
from Player import Player
import pygame

pygame.init()
prozor = pygame.display.set_mode((1280, 720))
sat = pygame.time.Clock()
txt_trava = pygame.image.load("images//grass.png")
txt_kuca = pygame.image.load("images//kuca.png")
txt_house_floor = pygame.image.load("images//housefloor.png")
txt_kuca = pygame.transform.scale(
    txt_kuca, (txt_kuca.get_width() * 0.69, txt_kuca.get_height() * 0.69)
)


zidovi = []


def dictToPlayer(d):
    p1 = Player(d["x"], d["y"], d["id"], d["money"])
    p1.team = d["team"]
    return p1


# haha


def handle_server(client_socket):
    global players
    con = client_socket
    while True:
        try:
            data = con.recv(4096)
            data = data.decode()
            data = str(data)
            if data != "":
                print(data)
                if data.startswith("heartbeat:"):
                    beatid = data.split("")[1]
                    client_socket.sendall(f"heartbeat_received:{beatid}".encode())
                if data.startswith("players:"):
                    dat = data.split("players:")[1]
                    players2 = json.loads(dat)
                    while len(players)<len(players2):
                        players.append(0)
                    for i in range(len(players2)):
                        players[i] = dictToPlayer(json.loads(players2[i]))
                        print("got players")

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
            pass


SERVER_HOST = "192.168.1.107"
SERVER_PORT = 14242
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))


thread_server_handler = threading.Thread(target=handle_server, args=[client_socket])
thread_server_handler.start()
frame_count = 0

players = []

client_socket.sendall("set_team:bank".encode())


def nacrtaj_mapu():

    prozor.fill("green")

    """
    for i in range(3):
        for j in range(4):
            prozor.blit(txt_trava, (j * 320, i * 320))
    

    """
    prozor.blit(txt_kuca, (120, 60))
    prozor.blit(txt_kuca, (500, 60))
    for zid in zidovi:
        pygame.draw.rect(prozor, pygame.Color("red"), zid)


def game():
    program_radi = True
    frame_count = 0
    while program_radi:
        if frame_count % 60 == 0:
            try:
                client_socket.sendall("heartbeat_received".encode())
            except Exception as e:
                print(e)
                if "10054" in str(e) or "timed out" in str(e):
                    break
                pass

        frame_count += 1
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit()
        nacrtaj_mapu()
        for player in players:
            player.draw(prozor)
            print(f"Rendered player @{player.x, player.y}")
        pygame.display.update()

        sat.tick(60)
        print(sat)


game()
