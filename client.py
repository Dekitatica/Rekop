

"""
import threading
import sys
import socket
import json

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 14242

def handle_server(client_socket):
    con = client_socket
    while True:
        try:
            data = con.recv(1024)
            data = data.decode()
            data = str(data)
            if data!="":
                print(data)

                

        except Exception as e:
            print(e)
            pass



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up some constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROWS = 8
COLUMNS = 8

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to draw the chessboard
def draw_chessboard():
    square_width = SCREEN_WIDTH // COLUMNS
    square_height = SCREEN_HEIGHT // ROWS

    for row in range(ROWS):
        for column in range(COLUMNS):
            color = WHITE if (row + column) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (column * square_width, row * square_height, square_width, square_height))

    # Draw the lines
    for row in range(ROWS + 1):
        pygame.draw.line(screen, BLACK, (0, row * square_height), (SCREEN_WIDTH, row * square_height), 2)
    for column in range(COLUMNS + 1):
        pygame.draw.line(screen, BLACK, (column * square_width, 0), (column * square_width, SCREEN_HEIGHT), 2)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    draw_chessboard()
    pygame.display.flip()