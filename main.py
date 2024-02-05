import os
import sys

import pygame
import requests


def get_map(lan, lat, spn, type_map):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={lan},{lat}&spn={spn[0]},{spn[1]}&l={type_map}"
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
            if event.key == pygame.K_UP:
                lan -= 1
            if event.key == pygame.K_DOWN:
                lan += 1
            if event.key == pygame.K_RIGHT:
                lat -= 1
            if event.key == pygame.K_LEFT:
                lat += 1
            get_map(lan, lat, spn, type_map)
    screen.fill("black")
    screen.blit(pygame.image.load(map_file), (0, 0))
pygame.quit()

os.remove(map_file)