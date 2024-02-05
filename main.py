import os
import sys

import pygame
import pygame_gui
import requests


BLACK = "black"



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


def btn_clk(event):
    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
        print("Press")


map_file = "map.png"

lan, lat, spn = 43.024616, 44.681771, [0.02, 0.02]
type_map = "map"

get_map(lan, lat, spn, type_map)

pygame.init()
screen = pygame.display.set_mode((600, 550))
manager = pygame_gui.UIManager((600, 550))
screen.blit(pygame.image.load(map_file), (0, 100))
pygame.display.flip()
run = True
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((450, 10, 140, 70)), text='Открыть', manager=manager)
text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((10, 10, 430, 70)), manager=manager)
clock = pygame.time.Clock()
while run:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if button.check_pressed():
            print("Press")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                spn[0] *= 2
                spn[1] *= 2
                get_map(lan, lat, spn, type_map)
            if event.key == pygame.K_PAGEDOWN:
                spn[0] /= 2
                spn[1] /= 2
                get_map(lan, lat, spn, type_map)
            if event.key == pygame.K_UP:
                lan -= 0.0005
            if event.key == pygame.K_DOWN:
                lan += 0.0005
            if event.key == pygame.K_RIGHT:
                lat += 0.0005
            if event.key == pygame.K_LEFT:
                lat -= 0.0005
            get_map(lan, lat, spn, type_map)
        manager.process_events(event)
    manager.update(time_delta)
    screen.blit(pygame.image.load(map_file), (0, 100))
    manager.draw_ui(screen)
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
