import threading
import sys
import socket
import json
from Player import Player
import pygame
import server
import time

pygame.init()
prozor = pygame.display.set_mode((1280, 720))
sat = pygame.time.Clock()
txt_trava = pygame.image.load("images//grass.png")
txt_kuca = pygame.image.load("images//kuca.png")
txt_house_floor = pygame.image.load("images//housefloor.png")
txt_bank = pygame.image.load("images//bank.png")


txt_laptop = pygame.image.load("images//imageedit_2_6652470183.png")
txt_kuca = pygame.transform.scale(
    txt_kuca, (txt_kuca.get_width() * 0.69, txt_kuca.get_height() * 0.69)
)
font = pygame.font.Font(None, 30)
txt_house_floor = pygame.transform.scale(
    txt_house_floor,
    (txt_house_floor.get_width() * 0.8, txt_house_floor.get_height() * 0.8),
)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
zidovi = []

cx = 0
cy = 0


def dictToPlayer(d):
    p1 = Player(d["x"], d["y"], d["id"], d["money"])
    p1.team = d["team"]
    return p1


def dictToTeam(d):
    t1 = server.Team(d["name"])
    t1.money = int(d["money"])
    t1.members = d["members"]
    t1.upgrades = d["upgrades"]
    t1.multip = d["multip"]
    return t1


selfPlayer = None
stupidlist = []
selfid = None
team = "nah"
font_upgrade = pygame.font.Font(None, 60)
txt_cas = pygame.image.load("Images//casino.png")
txt_cas = pygame.transform.scale(txt_cas, (1280, 720))


class Dugme:
    def __init__(self, tekst, rect, boja):
        self.tekst = tekst
        self.rect = rect
        self.boja = boja


def nacrtaj_dugme_bez_centiranja(dugme: Dugme):
    pygame.draw.rect(prozor, dugme.boja, dugme.rect)
    prozor.blit(dugme.tekst, dugme.rect.topleft)


btn_buy_miner = Dugme(
    font_upgrade.render("Upgrade Miner", True, (255, 255, 255)),
    pygame.Rect(460, 550, 320, 60),
    pygame.Color("black"),
)

teams_dict = {}
dealer_cards = 0
my_cards = 0
blj_updates = []
def handle_server(client_socket):
    global players
    global zidovi
    global selfPlayer
    global stupidlist
    global selfid
    global teams
    global my_cards
    global dealer_cards
    con = client_socket
    global blj_updates
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
                if data.startswith("teams?"):
                    dat = data.split("?")[1]
                    dat = json.loads(dat)
                    teams_dict["bank"] = dictToTeam(json.loads(dat["bank"]))
                    teams_dict["hero"] = dictToTeam(json.loads(dat["hero"]))
                    a = 5
                if data.startswith("dealer_cards?"):
                    dat = data.split("?")[1]
                    dealer_cards = json.loads(dat)
                if data.startswith("your_cards?"):
                    dat = data.split("?")[1]
                    my_cards = json.loads(dat)
                if data.startswith("blj_end?"):
                    dat = data.split("?")[1]
                    dat = dat.split(";")
                    d1 = {
                        "wl" : dat[0],
                        "your_cards" : json.loads(dat[1]),
                        "dealer_cards" : json.loads(dat[2]),
                        "bet" : int(dat[3])
                        
                    }
                    blj_updates.append(d1)
                    
                


        except Exception as e:
            print(e)
            if "10054" in str(e) or "timed out" in str(e):
                return
            pass


dugme_font = pygame.font.SysFont("Consolas", 60)
main_menu_dugme_quit = Dugme(
    dugme_font.render("EXIT", True, (255, 255, 255)),
    pygame.Rect(560, 465, 150, 60),
    pygame.Color("black"),
)
main_menu_dugme_credits = Dugme(
    dugme_font.render("CREDITS", True, (255, 255, 255)),
    pygame.Rect(520, 300, 245, 60),
    pygame.Color("black"),
)
credits_to_main_menu_button = Dugme(
    dugme_font.render("BACK", True, (255, 255, 255)),
    pygame.Rect(22, 470, 200, 60),
    pygame.Color("black"),
)
main_menu_play_button = Dugme(
    dugme_font.render("PLAY", True, (255, 255, 255)),
    pygame.Rect(560, 180, 150, 60),
    pygame.Color("black"),
)
miners_team_button = Dugme(
    dugme_font.render("Miner", True, (255, 255, 255)),
    pygame.Rect(100, 270, 245, 60),
    pygame.Color("black"),
)
bank_team_button = Dugme(
    dugme_font.render("Bank", True, (255, 255, 255)),
    pygame.Rect(750, 270, 245, 60),
    pygame.Color("black"),
)


selfMinerLevel = 1

players = []


def nacrtaj_mapu():
    global selfPlayer
    global selfid
    global playerRect
    global players
    prozor.fill("green")

    """
    for i in range(3):
        for j in range(4):
            prozor.blit(txt_trava, (j * 320, i * 320))
    
    """

    # prozor.blit(txt_kuca, (500, 60))
    # for zid in zidovi:
    #    pygame.draw.rect(prozor, pygame.Color("red"), zid)
    if selfPlayer != None:
        for player in players:
            try:
                if player.id == selfid:
                    selfPlayer = player
            except Exception as e:
                print(f"RARE: Type Error (~170)")
            playerRect = pygame.Rect(selfPlayer.x, selfPlayer.y, 35, 65)
        # pygame.draw.rect(prozor, pygame.Color("red"), playerRect, 5)
        # pygame.draw.rect(
        #    prozor,
        #    pygame.Color("red"),
        #    pygame.Rect(
        #       200, 130, txt_kuca.get_width() * 0.6, txt_kuca.get_height() * 0.6
        #    ),
        #    5,
        # )

        # for zid in zidovi:
        #    pygame.draw.rect(prozor, pygame.Color("red"), zid)

        change_house_layer(players)


def change_house_layer(players):
    global playerrect
    k1 = True
    k2 = True

    for player in players:
        try:
            playerrect = pygame.Rect(player.x, player.y, 35, 65)
        except Exception as e:
            time.sleep(1)
            playerrect = pygame.Rect(player.x, player.y, 35, 65)
            pass
        if (
            playerrect.colliderect(
                pygame.Rect(
                    200 - cx,
                    130 - cy,
                    txt_kuca.get_width() * 0.6,
                    txt_kuca.get_height() * 0.6,
                )
            )
            and k1
        ):
            prozor.blit(txt_house_floor, (200, 130))
            prozor.blit(txt_laptop, (280, 120))
            k1 = False
        if (
            playerrect.colliderect(
                pygame.Rect(
                    580, 130, txt_kuca.get_width() * 0.6, txt_kuca.get_height() * 0.6
                )
            )
            and k2
        ):
            prozor.blit(txt_house_floor, (580, 130))
            prozor.blit(txt_laptop, (660, 120))
            k2 = False

    if k1:
        prozor.blit(txt_kuca, (120, 60))
    if k2:
        prozor.blit(txt_kuca, (500, 60))


def create_transparent_rect(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)





def MinersUpgradeMenu():
    create_transparent_rect(prozor, (0, 0, 0, 127), (20, 20, 1240, 680))

    nacrtaj_dugme_bez_centiranja(btn_buy_miner)
    if (
        teams_dict != None
        and selfPlayer != None
        and selfPlayer.team != "na"
        and len(teams_dict.keys()) != 0
    ):
        upgrade_level_text = font_upgrade.render(
            f"Upgrade Level : {teams_dict[selfPlayer.team].latest_upgrade}",
            False,
            pygame.Color("black"),
        )
        prozor.blit(upgrade_level_text, (80, 150))





def team_selector():
    global team
    program_radi = True
    while program_radi:
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                quit()
            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                if miners_team_button.rect.collidepoint(dogadjaj.pos):
                    team = "hero"
                    game()
                if bank_team_button.rect.collidepoint(dogadjaj.pos):
                    team = "bank"


                    game()

        prozor.fill(pygame.Color("cyan"))
        nacrtaj_dugme_bez_centiranja(miners_team_button)
        nacrtaj_dugme_bez_centiranja(bank_team_button)
        pygame.display.update()


def game():
    global selfMinerLevel
    global selfPlayer
    global playerRect
    global stupidlist
    global team
    global cx
    global cy
    program_radi = True
    frame_count = 0
    SERVER_HOST = "127.0.0.1"


    SERVER_PORT = 14242

    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print("Connected")

    thread_server_handler = threading.Thread(target=handle_server, args=[client_socket])
    thread_server_handler.start()
    frame_count = 0

    client_socket.sendall(f"set_team?{team}|".encode())
    while program_radi:
        if frame_count % 60 == 0:
            try:
                client_socket.sendall(f"heartbeat_received?{frame_count}|".encode())
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

                    client_socket.sendall(f"buy_upgrade?".encode())
                    selfMinerLevel += 1
        keys = pygame.key.get_pressed()

        important_keys = {"w": False, "s": False, "a": False, "d": False}

        if keys[pygame.K_w]:
            important_keys["w"] = True
            # cy+=1
        if keys[pygame.K_s]:
            important_keys["s"] = True
            # cy-=1
        if keys[pygame.K_a]:
            important_keys["a"] = True
            # cx+=1
        if keys[pygame.K_d]:
            important_keys["d"] = True
            # cx+-1

        for key in important_keys.keys():
            if important_keys[key] == True:
                obj = json.dumps(important_keys)
                client_socket.sendall(f"request_move?{obj}|".encode())
                break

        nacrtaj_mapu()

        for player in players:
            if type(player) == Player:
                player.draw(prozor)

                print(f"{player.x , player.y}")
                playerrect = pygame.Rect(player.x, player.y, 35, 65)

                laptoprect = pygame.Rect(

                    280, 120, txt_laptop.get_width(), txt_laptop.get_height()
                )
                if playerrect.colliderect(laptoprect) or playerrect.colliderect(
                    pygame.Rect(
                        660, 120, txt_laptop.get_width(), txt_laptop.get_height()
                    )
                ):
                    MinersUpgradeMenu()
                # print(f"Rendered player @{player.x, player.y}")

        fps_text = font.render(
            f"FPS : {round(sat.get_fps() , 0)}", False, pygame.Color("black")
        )
        # MinersUpgradeMenu()
        prozor.blit(fps_text, (0, 0))

        pygame.display.update()

        sat.tick(60)


text_credits_luka = font.render(
    "Developer : Luka Markovic", False, pygame.Color("white")
)
text_credits_deki = font.render(
    "Developer : Dejan Livada", False, pygame.Color("white")
)
#deki = pygame.image.load("images//specijalan.jpeg")
#deki = pygame.transform.scale(deki, (300, 400))
#deki = pygame.transform.rotate(deki, -90)


def main_menu():
    program_radi = True
    while program_radi:
        prozor.fill((pygame.Color("cyan")))

        nacrtaj_dugme_bez_centiranja(main_menu_dugme_quit)
        nacrtaj_dugme_bez_centiranja(main_menu_dugme_credits)
        nacrtaj_dugme_bez_centiranja(main_menu_play_button)
 
        mouse_state = pygame.mouse.get_pressed()
        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                program_radi = False
                sys.exit() 

            if dogadjaj.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_dugme_quit.rect.collidepoint(dogadjaj.pos):
                    program_radi = False
                    pygame.quit()
                    sys.exit()
                if main_menu_dugme_credits.rect.collidepoint(dogadjaj.pos):
                    game_credits()
                if main_menu_play_button.rect.collidepoint(dogadjaj.pos):
                    team_selector()
        mouse_pos = pygame.mouse.get_pos()
        pygame.display.update()
        sat.tick(60)


def game_credits():
    credits_speed = 0
    credits_timer = 5
    program_radi = True

    while program_radi:
        for dogadjaj in pygame.event.get():
            if dogadjaj == pygame.QUIT:
                program_radi = False
        credits_speed += 0.2
        prozor.fill(pygame.Color("cyan"))
        prozor.blit(text_credits_deki, (580, credits_speed))
       # prozor.blit(deki, (580, -400 + credits_speed))
        prozor.blit(text_credits_luka, (640, -700 + credits_speed))
        credits_timer -= 0.001
        if credits_timer < 0:
            return
        pygame.display.update()


temp_player = pygame.Rect(50, 50, 40, 60)


lista_zidova = [
    pygame.Rect(20, 50, 1235, 1),
    pygame.Rect(205, 190, 205, 100),
    pygame.Rect(520, 175, 235, 110),
    pygame.Rect(865, 190, 210, 110),
    # pygame.Rect(1105, 290, 50, 125),

    # pygame.Rect(775, 290, 55, 120),
    # pygame.Rect(445, 290, 50, 125),
    # pygame.Rect(115, 290, 55, 120),
    pygame.Rect(100, 475, 210, 125),
    pygame.Rect(465, 460, 105, 195),
    pygame.Rect(705, 450, 105, 210),
    pygame.Rect(970, 465, 205, 115),
    pygame.Rect(1180, 660, 25, 25),
    pygame.Rect(70, 660, 30, 20),
    pygame.Rect(20, 50, 2, 645),
    pygame.Rect(20, 695, 575, 2),
    pygame.Rect(680, 695, 575, 2),
    pygame.Rect(1255, 50, 2, 640),
]


def cas():
    global temp_player
    program_radi = True
    while program_radi:                                                                                     
        for dogadjaj in pygame.event.get():                                                                                     
            if dogadjaj.type == pygame.QUIT:                                                                                     
                program_radi = False                                                                                     
                sys.exit()                                                                                     
        prozor.blit(txt_cas, (0, 0))                                                                                     
        pygame.draw.rect(prozor, pygame.Color("blue"), temp_player)                                                                                     
        for zid in lista_zidova:                                                                                     
            pygame.draw.rect(prozor, pygame.Color("red"), zid, 5)                                                                                     
                                                                                     
        keys = pygame.key.get_pressed()                                                      


        if keys[pygame.K_w]:                                                                                     
            temp_player.y -= 5                                                                                     
        if keys[pygame.K_s]:                                                                                     
            temp_player.y += 5                                                                                     
        if keys[pygame.K_d]:                                                                                     
            temp_player.x += 5                                                                                     
        if keys[pygame.K_a]:                                                                                     
            temp_player.x -= 5                                                                                     
        print(f"{temp_player.x} {temp_player.y} ")                                                                                     

       # if temp_player.colliderect()





        pygame.display.update()                                                                                     
                                                                                     
                                                                                     
main_menu()                                                                                     
#cas()                                                                                     
                                                                                     