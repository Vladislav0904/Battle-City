import pygame
import os
import sys
import random
from game_over import game_over


def terminate():
    pygame.quit()
    sys.exit()


def game_is_over():
    game_over()


def load_image(name, color_key=None):
    fullname = os.path.join('data/assets', name)
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = os.path.join('data/assets', filename)
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_sound(filename):
    filename = os.path.join('data/sounds', filename)
    sound = pygame.mixer.Sound(filename)
    return sound


def game(players=1):
    direction = 'up'
    direction2 = 'up'
    last = 1
    last2 = 1
    if players == 1:
        coop = False
    elif players == 2:
        coop = True

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.tile_type = tile_type
            self.image = tile_images[tile_type]
            self.x = pos_x
            self.y = pos_y
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = player_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x + 15, tile_height * pos_y + 5)
            self.mask = pygame.mask.from_surface(self.image)
            self.cool_down = False

        def update(self):
            for i in tiles_group:
                if (str(i.tile_type) == 'wall' or str(i.tile_type) == 'armor') \
                        and pygame.sprite.collide_mask(self, i):
                    print(1)
                    if abs(i.rect.top - self.rect.bottom) < 10:
                        print(1)
                        return 'down'
                    if abs(i.rect.bottom - self.rect.top) < 10:
                        print(2)
                        return 'up'
                    if abs(i.rect.right - self.rect.left) < 10:
                        print(3)
                        return 'left'
                    if abs(i.rect.left - self.rect.right) < 10:
                        print(4)
                        return 'right'
            return True

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direct, sender):
            super().__init__(all_sprites)
            self.sender = sender
            self.direction = direct
            self.speed = 5
            self.image = pygame.Surface((3, 8))
            self.image.fill(pygame.Color('gray'))
            self.rect = self.image.get_rect()
            if self.direction == 'up':
                self.rect = self.rect.move(x + 10, y)
            elif self.direction == 'down':
                self.rect = self.rect.move(x + 10, y + 20)
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'right':
                self.rect = self.rect.move(x + 20, y + 10)
                self.image = pygame.transform.rotate(self.image, -90)
            elif self.direction == 'left':
                self.rect = self.rect.move(x - 20, y + 10)
                self.image = pygame.transform.rotate(self.image, 90)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            global on_cool_down
            if self.direction == 'up':
                self.rect.y -= self.speed
            elif self.direction == 'down':
                self.rect.y += self.speed
            elif self.direction == 'right':
                self.rect.x += self.speed
            elif self.direction == 'left':
                self.rect.x -= self.speed

            for i in tiles_group:
                if str(i.tile_type) == 'wall' and pygame.sprite.collide_mask(self, i):
                    self.kill()
                    if self.sender == 1:
                        player.cool_down = False
                    elif self.sender == 2:
                        player2.cool_down = False
                    Tile('empty_small', i.x, i.y)
                    explosion = AnimatedSprite(load_image("explosion.png"), 3, 1, self.rect.x - 10, self.rect.y)
                    i.kill()
                elif str(i.tile_type) == 'fort' and pygame.sprite.collide_mask(self, i):
                    self.kill()
                    if self.sender == 1:
                        player.cool_down = False
                    elif self.sender == 2:
                        player2.cool_down = False
                    # Tile('empty_small', i.x, i.y)
                    explosion = AnimatedSprite(load_image("explosion.png"), 3, 1, self.rect.x - 10, self.rect.y)
                    i.kill()
                    game_over()
                    if self.sender == 1:
                        player.cool_down = False
                    elif self.sender == 2:
                        player2.cool_down = False
                elif str(i.tile_type) != 'empty' and str(i.tile_type) != 'empty_small' \
                        and pygame.sprite.collide_mask(self, i):
                    self.kill()
                    player.cool_down = False
                    explosion = AnimatedSprite(load_image("explosion.png"), 3, 1, self.rect.x - 10, self.rect.y)
            if self.rect.y < -10 or self.rect.x < -10 or self.rect.x > 850 or self.rect.y > 650:
                self.kill()
                if self.sender == 1:
                    player.cool_down = False
                elif self.sender == 2:
                    player2.cool_down = False

    class AnimatedSprite(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__(all_sprites)
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x, y)
            self.counter = 1

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                    sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)))

        def update(self):
            if self.counter <= 3:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.counter += 1
            else:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.pos_x = 1
            self.pos_y = 1
            self.image = enemy_image
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)

    def generate_level(level):
        new_player, x, y = None, None, None
        second_player = None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '*':
                    Tile('armor', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                elif level[y][x] == '/':
                    Tile('empty', x, y)
                    if coop:
                        second_player = Player(x, y)
                elif level[y][x] == '!':
                    Tile('fort', x, y)

        # вернем игрока, а также размер поля в клетках
        return new_player, x, y, second_player

    tile_images = {
        'wall': load_image('brick2.png'),
        'empty': load_image('empty.png'),
        'empty_small': load_image('empty_small.png'),
        'armor': load_image('mesh.png'),
        'fort': load_image('fort.png')
    }
    player_image = load_image('player_tank.png')
    enemy_image = load_image('enemy_tank.png')

    tile_width, tile_height = 48, 24
    # основной персонаж
    player = None
    player2 = None

    # группы спрайтов
    start_ticks = pygame.time.get_ticks()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    player, level_x, level_y, player2 = generate_level(load_level('map.txt'))
    clock = pygame.time.Clock()
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    enemy = Enemy(6, 1)
    move_left2 = False
    move_right2 = False
    move_up2 = False
    move_down2 = False
    i = 1
    move = load_sound('player_move.wav')
    move.set_volume(0.3)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    if not player.cool_down:
                        Bullet(player.rect.x, player.rect.y, direction, 1)
                        shot = load_sound('shot.wav')
                        shot.play()
                        player.cool_down = True
                if keys[pygame.K_RIGHT]:
                    move_right = True
                if keys[pygame.K_LEFT]:
                    move_left = True
                if keys[pygame.K_UP]:
                    move_up = True
                if keys[pygame.K_DOWN]:
                    move_down = True
            elif event.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                if not keys[pygame.K_RIGHT]:
                    move_right = False
                if not keys[pygame.K_LEFT]:
                    move_left = False
                if not keys[pygame.K_UP]:
                    move_up = False
                if not keys[pygame.K_DOWN]:
                    move_down = False
            elif coop:
                if event.type == pygame.JOYAXISMOTION:
                    if pygame.joystick.Joystick(0).get_axis(0) > 0.5:
                        move_right2 = True
                    elif pygame.joystick.Joystick(0).get_axis(0) < -0.5:
                        move_left2 = True
                    else:
                        move_left2 = False
                        move_right2 = False
                    if pygame.joystick.Joystick(0).get_axis(1) > 0.5:
                        move_down2 = True
                    elif pygame.joystick.Joystick(0).get_axis(1) < -0.5:
                        move_up2 = True
                    else:
                        move_up2 = False
                        move_down2 = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    if pygame.joystick.Joystick(0).get_button(1):
                        if not player2.cool_down:
                            Bullet(player2.rect.x, player2.rect.y, direction2, 2)
                            shot = load_sound('shot.wav')
                            shot.play()
                            player2.cool_down = True

        if move_right or move_left or move_down or move_up:
            if i <= 1:
                move.play()
                i += 1
        else:
            move.stop()
            i = 1
        if move_right and player.update() != 'right':
            player.rect.x += 4
            player.image = pygame.transform.rotate(player_image, -90)
            direction = 'right'
        elif move_left and player.update() != 'left':
            player.rect.x -= 4
            player.image = pygame.transform.rotate(player_image, 90)
            direction = 'left'
        elif move_up and player.update() != 'up':
            player.rect.y -= 4
            player.image = player_image
            direction = 'up'
        elif move_down and player.update() != 'down':
            player.rect.y += 4
            player.image = pygame.transform.rotate(player_image, 180)
            direction = 'down'
        if coop:
            if move_right2 and player2.update() != 'right':
                player2.rect.x += 4
                player2.image = pygame.transform.rotate(player_image, -90)
                direction2 = 'right'
            elif move_left2 and player2.update() != 'left':
                player2.rect.x -= 4
                player2.image = pygame.transform.rotate(player_image, 90)
                direction2 = 'left'
            elif move_up2 and player2.update() != 'up':
                player2.rect.y -= 4
                player2.image = player_image
                direction2 = 'up'
            elif move_down2 and player2.update() != 'down':
                player2.rect.y += 4
                player2.image = pygame.transform.rotate(player_image, 180)
                direction2 = 'down'
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
FPS = 30
size = width, height = 816, 624
screen = pygame.display.set_mode(size)
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.event.pump()
