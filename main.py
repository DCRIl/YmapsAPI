import pygame

pygame.init()
screen = pygame.display.set_mode((700, 700))

run = True
while run:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
