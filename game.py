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
font = pygame.font.Font(None, 30)

toggle_fps = False
zidovi = []


def dictToPlayer(d):
    p1 = Player(d["x"], d["y"], d["id"], d["money"])
    p1.team = d["team"]
    return p1


selfPlayer = None


def handle_server(client_socket):
    global players
    global zidovi
    global selfPlayer
    con = client_socket
    while True:
        try:
            data = con.recv(4096)
            data = data.decode()
            data = str(data)
            if data != "":
                print(data)
                if data.startswith("heartbeat%"):
                    beatid = data.split("%")[1]
                    client_socket.sendall(f"heartbeat_received:{beatid}".encode())
                if data.startswith("players%"):
                    dat = data.split("players%")[1]
                    players2 = json.loads(dat)
                    while len(players) < len(players2):
                        players.append(0)
                    for i in range(len(players2)):
                        players[i] = dictToPlayer(json.loads(players2[i]))
                        print("got players")
                if data.startswith("worlddata%"):
                    dat = data.split("worlddata%")[1]
                    world_info = json.loads(dat)
                    world_info["walls"] = [
                        pygame.Rect(x, y, w, h) for x, y, w, h in world_info["walls"]
                    ]
                    zidovi = world_info["walls"]
                    print("got worlddata")
                if data.startswith("id%"):
                    dat = data.split("id%")
                    for player in players:
                        if player.id == dat[1]:
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
    # for zid in zidovi:
    #    pygame.draw.rect(prozor, pygame.Color("red"), zid)



def change_house_layer():
    pass


def create_transparent_rect(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


playerRect = None

def check_col():
    pass



def game():
    global toggle_fps
    global selfPlayer
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
        if type(selfPlayer) == Player:
            playerRect = pygame.Rect(selfPlayer.x, selfPlayer.y, 35, 65)
            print(playerRect)
        frame_count += 1
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit()

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
                client_socket.sendall(f"request_move%{obj}".encode())
                break

        nacrtaj_mapu()

        for player in players:
            if type(player) == Player:
                player.draw(prozor)
                print(f"Rendered player @{player.x, player.y}")
        fps_text = font.render(
            f"FPS : {round(sat.get_fps() , 0)}", False, pygame.Color("black")
        )
        create_transparent_rect(prozor , pygame.Color("black") , pygame.Rect(0,0,1280,720))
        prozor.blit(fps_text, (0, 0))
        pygame.display.update()

        sat.tick(60)


game()
