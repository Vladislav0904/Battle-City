import pygame
import os
import game_level


# загрузка музыки в игру
def load_sound(filename):
    filename = os.path.join('data/sounds', filename)
    sound = pygame.mixer.Sound(filename)
    return sound


# создание загрузочного экрана между уровнями
def stage_load(is_coop, number):
    if number != 6:
        pygame.init()
        width = 800
        height = 600
        FPS = 60
        screen = pygame.display.set_mode((width, height))
        clock = pygame.time.Clock()
        pygame.display.set_caption('Battle City')
        stage = load_sound('stage.wav')
        screen.fill((128, 128, 128))
        font = pygame.font.Font('./data/fonts/PixelEmulator-xq08.ttf', 48)
        text = font.render(f"STAGE {number}", True, (255, 255, 255))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
        stage.play()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        game_level.game(is_coop, number)

            pygame.display.flip()
            clock.tick(FPS)
        manager.update(FPS / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)
