import pygame
import pygame_gui
import sys
import os

pygame.init()
width = 800
height = 600
FPS = 60
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Battle City')


# выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# создаёт окно завершения игры
def game_over():
    font = pygame.font.Font('./data/fonts/BRICK.ttf', 100)
    text = font.render("GAME", True, (211, 71, 46))
    text1 = font.render("OVER", True, (211, 71, 46))
    text_x = width // 2 - text.get_width() // 2
    text_y = 50
    text_x1 = width // 2 - text.get_width() // 2 + 25
    text_y1 = 160
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (text_x1, text_y1))
    manager = pygame_gui.UIManager((width, height), os.path.join('data', 'main_menu.json'))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)
        manager.update(FPS / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
    manager.update(FPS / 1000)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(FPS)
