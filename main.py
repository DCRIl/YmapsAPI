import os
import sys

import pygame
import requests


BLACK = "black"


class TextInput:
    def __init__(self, x, y, width, height, color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = ""
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def add_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


def get_map(lan, lat, spn, type_map):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={lat},{lan}&spn={spn[0]},{spn[1]}&l={type_map}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

map_file = "map.png"

lan, lat, spn = 43.024616, 44.681771, [0.02, 0.02]
type_map = "map"

get_map(lan, lat, spn, type_map)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_9:
                spn[0] *= 2
                spn[1] *= 2
                get_map(lan, lat, spn, type_map)
            if event.key == pygame.K_3:
                spn[0] /= 2
                spn[1] /= 2
                get_map(lan, lat, spn, type_map)
            if event.key == pygame.K_UP:
                lan -= 0.005
            if event.key == pygame.K_DOWN:
                lan += 0.005
            if event.key == pygame.K_RIGHT:
                lat += 0.005
            if event.key == pygame.K_LEFT:
                lat -= 0.005
            get_map(lan, lat, spn, type_map)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
