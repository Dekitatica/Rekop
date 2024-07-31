import threading
import sys
import socket
import json
from Player import Player
import pygame

from menu import Dugme, nacrtaj_dugme_bez_centiranja

pygame.init()
prozor = pygame.display.set_mode((1280, 720))
sat = pygame.time.Clock()
txt_trava = pygame.image.load("images//grass.png")
txt_kuca = pygame.image.load("images//kuca.png")
txt_house_floor = pygame.image.load("images//housefloor.png")
txt_kuca = pygame.transform.scale(
    txt_kuca, (txt_kuca.get_width() * 0.69, txt_kuca.get_height() * 0.69)
)
font = pygame.font.Font(None, 30)
txt_house_floor = pygame.transform.scale(
    txt_house_floor,
    (txt_house_floor.get_width() * 0.8, txt_house_floor.get_height() * 0.8),
)

zidovi = []


def dictToPlayer(d):
    p1 = Player(d["x"], d["y"], d["id"], d["money"])
    p1.team = d["team"]
    return p1


selfPlayer = None
stupidlist = []
selfid = None

font_upgrade = pygame.font.Font(None, 60)


btn_buy_miner = Dugme(
    font_upgrade.render("Upgrade Miner", True, (255, 255, 255)),
    pygame.Rect(460, 550, 320, 60),
    pygame.Color("black"),
)


def handle_server(client_socket):
    global players
    global zidovi
    global selfPlayer
    global stupidlist
    global selfid
    con = client_socket
    while True:
        try:
            data = con.recv(4096)
            data = data.decode()
            data = str(data)
            if data != "":
                # print(data)
                if data.startswith("heartbeat?"):
                    beatid = data.split("?")[1]
                    client_socket.sendall(f"heartbeat_received:{beatid}|".encode())
                if data.startswith("players?"):
                    dat = data.split("players?")[1]
                    players2 = json.loads(dat)
                    while len(players) < len(players2):
                        players.append(0)
                    for i in range(len(players2)):
                        players[i] = dictToPlayer(json.loads(players2[i]))
                        # print("got players")
                if data.startswith("worlddata?"):
                    dat = data.split("worlddata?")[1]
                    world_info = json.loads(dat)
                    world_info["walls"] = [
                        pygame.Rect(x, y, w, h) for x, y, w, h in world_info["walls"]
                    ]
                    zidovi = world_info["walls"]
                    print("got worlddata")
                if data.startswith("id?"):
                    dat = data.split("id?")
                    for player in players:
                        if player.id == dat[1]:
                            selfid = player.id
                            selfPlayer = player

        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
            pass


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 14242
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
print("Connected")

thread_server_handler = threading.Thread(target=handle_server, args=[client_socket])
thread_server_handler.start()
frame_count = 0

players = []

client_socket.sendall("set_team?bank|".encode())
selfMinerLevel = 0

def nacrtaj_mapu():
    global selfPlayer
    global selfid
    global playerRect
    prozor.fill("green")

    """
    for i in range(3):
        for j in range(4):
            prozor.blit(txt_trava, (j * 320, i * 320))
    

    """

    prozor.blit(txt_kuca, (500, 60))
    # for zid in zidovi:
    #    pygame.draw.rect(prozor, pygame.Color("red"), zid)
    if selfPlayer != None:
        for player in players:
            if player.id == selfid:
                selfPlayer = player
        playerRect = pygame.Rect(selfPlayer.x, selfPlayer.y, 35, 65)
        pygame.draw.rect(prozor, pygame.Color("red"), playerRect, 5)
        pygame.draw.rect(
            prozor,
            pygame.Color("red"),
            pygame.Rect(
                200, 130, txt_kuca.get_width() * 0.6, txt_kuca.get_height() * 0.6
            ),
            5,
        )
        print(playerRect)
        change_house_layer(playerRect)


def change_house_layer(playerrect):

    if playerrect.colliderect(
        pygame.Rect(200, 130, txt_kuca.get_width() * 0.6, txt_kuca.get_height() * 0.6)
    ):
        prozor.blit(txt_house_floor, (200, 130))
    else:
        prozor.blit(txt_kuca, (120, 60))


def create_transparent_rect(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def MinersUpgradeMenu():
    create_transparent_rect(prozor, (0, 0, 0, 127), (20, 20, 1240, 680))
    nacrtaj_dugme_bez_centiranja(btn_buy_miner)
    upgrade_level_text = font_upgrade.render(
        f"Upgrade Level : ?", False, pygame.Color("black")
    )
    prozor.blit(upgrade_level_text, (80, 150))


def game():
    global selfMinerLevel
    global selfPlayer
    global playerRect
    global stupidlist
    program_radi = True
    frame_count = 0
    while program_radi:
        if frame_count % 60 == 0:
            try:
                client_socket.sendall(f"heartbeat_received?{frame_count}|".encode())
                for i in range(1,6):
                    client_socket.sendall(f"buy_upgrade?{i}|".encode())
                print(f"Sent beat {selfPlayer.id}")
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
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                if btn_buy_miner.rect.collidepoint(dogadjaj.pos):

                    client_socket.sendall(f"buy_upgrade?{selfMinerLevel}".encode())
                    selfMinerLevel+= 1
        keys = pygame.key.get_pressed()

        important_keys = {"w": False, "s": False, "a": False, "d": False}

        if keys[pygame.K_w]:
            important_keys["w"] = True
        if keys[pygame.K_s]:
            important_keys["s"] = True
        if keys[pygame.K_a]:
            important_keys["a"] = True
        if keys[pygame.K_d]:
            important_keys["d"] = True

        for key in important_keys.keys():
            if important_keys[key] == True:
                obj = json.dumps(important_keys)
                client_socket.sendall(f"request_move?{obj}|".encode())
                break

        nacrtaj_mapu()

        for player in players:
            if type(player) == Player:
                player.draw(prozor)
                # print(f"Rendered player @{player.x, player.y}")
        fps_text = font.render(
            f"FPS : {round(sat.get_fps() , 0)}", False, pygame.Color("black")
        )
        MinersUpgradeMenu()
        prozor.blit(fps_text, (0, 0))
        pygame.display.update()

        sat.tick(60)


game()
