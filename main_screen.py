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


def terminate():
    pygame.quit()
    sys.exit()


def load_main_menu(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font('./data/fonts/BRICK.ttf', 100)
    text = font.render("BATTLE", True, (211, 71, 46))
    text1 = font.render("CITY", True, (211, 71, 46))
    text_x = width // 2 - text.get_width() // 2
    text_y = 50
    text_x1 = width // 2 - text.get_width() // 2 + 75
    text_y1 = 160
    screen.blit(text, (text_x, text_y))
    screen.blit(text1, (text_x1, text_y1))
    manager = pygame_gui.UIManager((width, height), os.path.join('data', 'main_menu.json'))
    f_player_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width // 2 - 75, 300), (150, 50)),
        text='1 PLAYER',
        manager=manager)
    s_player_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width // 2 - 75, 350), (150, 50)),
        text='2 PLAYER',
        manager=manager)
    construct_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((width // 2 - 125, height // 2 + 100), (250, 50)),
        text='CONSTRUCTION',
        manager=manager)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == f_player_btn:
                        print('debug btn output 1')
                    if event.ui_element == s_player_btn:
                        print('debug btn output 2')
                    if event.ui_element == construct_btn:
                        print('debug btn output 3')
            manager.process_events(event)
        manager.update(FPS / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
    manager.update(FPS / 1000)
    manager.draw_ui(screen)
    pygame.display.flip()
    clock.tick(FPS)


load_main_menu(screen)
