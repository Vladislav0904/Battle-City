import pygame
import os
import sys
import random
from game_over import game_over
import game_stage


def terminate():
    pygame.quit()
    sys.exit()


def game_is_over(pl1, pl2, multi):
    if multi:
        if pl1.is_Dead and pl2.is_Dead:
            game_over()
    elif not multi:
        if pl1.is_Dead:
            game_over()


def victory(coop, level):
    game_stage.stage_load(coop, level)


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
    filename = os.path.join('data/assets/', filename)
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


def game(players=1, level=1):
    direction = 'up'
    direction2 = 'up'
    last = 1
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
            self.lives = 3
            self.is_Dead = False
            self.kills = 0

        def update(self):
            collided = []
            for i in tiles_group:
                if (str(i.tile_type) == 'wall' or str(i.tile_type) == 'armor'
                    or str(i.tile_type) == 'water') \
                        and pygame.sprite.collide_mask(self, i):
                    print(1)
                    if abs(i.rect.top - self.rect.bottom) < 5:
                        print(1)
                        collided.append('down')
                    if abs(i.rect.bottom - self.rect.top) < 5:
                        print(2)
                        collided.append('up')
                    if abs(i.rect.right - self.rect.left) < 5:
                        print(3)
                        collided.append('left')
                    if abs(i.rect.left - self.rect.right) < 5:
                        print(4)
                        collided.append('right')
                if self.rect.x >= 600:
                    collided.append('right')
                if self.rect.x <= 0:
                    collided.append('left')
                if self.rect.y <= 0:
                    collided.append('up')
                if self.rect.y >= 585:
                    collided.append('down')
            return collided

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
                elif str(i.tile_type) == 'water' and pygame.sprite.collide_mask(self, i):
                    pass
                elif str(i.tile_type) == 'leaves' and pygame.sprite.collide_mask(self, i):
                    pass
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
                    if self.sender == 1:
                        player.cool_down = False
                    elif self.sender == 2:
                        player2.cool_down = False
                    explosion = AnimatedSprite(load_image("explosion.png"), 3, 1, self.rect.x - 10, self.rect.y)
            if self.rect.y < -10 or self.rect.x < -10 or self.rect.x > 850 or self.rect.y > 650:
                self.kill()
                if self.sender == 1:
                    player.cool_down = False
                elif self.sender == 2:
                    player2.cool_down = False
            for i in enemy_group:
                if pygame.sprite.collide_mask(self, i) and self.sender != 3:
                    self.kill()
                    i.kill()
                    explosion = AnimatedSprite(load_image("explosion.png"), 3, 1, self.rect.x - 10, self.rect.y)
                    i.is_dead = True
                    if self.sender == 1:
                        player.cool_down = False
                        player.kills += 1
                    elif self.sender == 2:
                        player2.cool_down = False
                        player2.kills += 1
            for i in player_group:
                if pygame.sprite.collide_mask(self, i) and self.sender != 1 and self.sender != 2:
                    if i == player:
                        i.rect.x = start_1[0]
                        i.rect.y = start_1[1]
                    elif i == player2:
                        i.rect.x = start_2[0]
                        i.rect.y = start_2[1]
                    i.lives -= 1
                if i.lives < 0:
                    i.is_Dead = True
                    game_is_over(player, player2, coop)

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
        def __init__(self, pos_x, pos_y, pos):
            super().__init__(all_sprites, enemy_group)
            self.image = enemy_image
            if pos == 1:
                self.direction = 'right'
            elif pos == 2:
                self.direction = 'left'
                self.image = pygame.transform.rotate(enemy_image, 180)
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.is_dead = False
            self.last = 1
            self.mask = pygame.mask.from_surface(self.image)

        def shoot(self):
            if not self.is_dead:
                Bullet(self.rect.x, self.rect.y, self.direction, 3)

        def update(self):
            collided = []
            if self.rect.x >= 600:
                print('gay')
                collided.append('right')
            if self.rect.x <= 0:
                collided.append('left')
                print('gay')
            if self.rect.y <= 0:
                collided.append('up')
            if self.rect.y >= 585:
                collided.append('down')
            for i in tiles_group:
                if (str(i.tile_type) == 'empty' or str(i.tile_type) == 'empty_small') and \
                        pygame.sprite.collide_mask(self, i):
                    dir = random.randint(1, 3)
                    for j in collided:
                        if 'up' in j:
                            if dir == 1:
                                self.direction = 'down'
                            elif dir == 2:
                                self.direction = 'left'
                            elif dir == 3:
                                self.direction = 'right'
                        elif 'down' in j:
                            if dir == 1:
                                self.direction = 'up'
                            elif dir == 2:
                                self.direction = 'left'
                            elif dir == 3:
                                self.direction = 'right'
                        elif 'right' in j:
                            if dir == 1:
                                self.direction = 'down'
                            elif dir == 2:
                                self.direction = 'left'
                            elif dir == 3:
                                self.direction = 'up'
                        elif 'left' in j:
                            if dir == 1:
                                self.direction = 'down'
                            elif dir == 2:
                                self.direction = 'up'
                            elif dir == 3:
                                self.direction = 'right'
                if (str(i.tile_type) == 'wall' or
                    str(i.tile_type) == 'armor' or
                    str(i.tile_type) == 'water') \
                        and pygame.sprite.collide_mask(self, i):
                    dir = random.randint(1, 5)
                    if self.direction == 'up':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3 or dir == 5:
                            self.direction = 'right'
                    elif self.direction == 'down':
                        if dir == 1:
                            self.direction = 'up'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3 or dir == 5:
                            self.direction = 'right'
                    elif self.direction == 'right':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3:
                            self.direction = 'up'
                    elif self.direction == 'left':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'up'
                        elif dir == 3 or dir == 5:
                            self.direction = 'right'
            for enemy in enemy_group:
                if pygame.sprite.collide_mask(self, enemy) and self != enemy:
                    dir = random.randint(1, 3)
                    if self.direction == 'up':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3:
                            self.direction = 'right'
                    elif self.direction == 'down':
                        if dir == 1:
                            self.direction = 'up'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3:
                            self.direction = 'right'
                    elif self.direction == 'right':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'left'
                        elif dir == 3:
                            self.direction = 'up'
                    elif self.direction == 'left':
                        if dir == 1:
                            self.direction = 'down'
                        elif dir == 2:
                            self.direction = 'up'
                        elif dir == 3:
                            self.direction = 'right'
            self.change_rotation(self.direction)
            if self.direction == 'up':
                self.rect.y -= 3
            elif self.direction == 'down':
                self.rect.y += 3
            elif self.direction == 'right':
                self.rect.x += 3
            elif self.direction == 'left':
                self.rect.x -= 3
            cool_down_shot = 1500
            now = pygame.time.get_ticks()
            if now - self.last >= cool_down_shot:
                self.last = now
                self.shoot()

        def change_rotation(self, rot):
            if rot == 'up':
                self.image = pygame.transform.rotate(enemy_image, 90)
            elif rot == 'down':
                self.image = pygame.transform.rotate(enemy_image, -90)
            elif rot == 'left':
                self.image = pygame.transform.rotate(enemy_image, 180)
            elif rot == 'right':
                self.image = enemy_image

    def generate_level(level):
        new_player, x, y = None, None, None
        second_player = None
        start_2 = None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == 's':
                    Tile('empty_small', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '*':
                    Tile('armor', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                    start_1 = (x * 48, y * 24)
                elif level[y][x] == '/':
                    Tile('empty', x, y)
                    if coop:
                        second_player = Player(x, y)
                        start_2 = (x * 48, y * 24)
                elif level[y][x] == '!':
                    Tile('empty_small', x, y)
                    Tile('fort', x, y)
                elif level[y][x] == 'l':
                    Tile('leaves', x, y)
                elif level[y][x] == 'w':
                    Tile('water', x, y)

        # вернем игрока, а также размер поля в клетках
        return new_player, x, y, second_player, start_1, start_2

    tile_images = {
        'wall': load_image('brick2.png'),
        'empty': load_image('empty.png'),
        'empty_small': load_image('empty_small.png'),
        'armor': load_image('mesh.png'),
        'fort': load_image('fort.png'),
        'leaves': load_image('leaves.png'),
        'water': load_image('water.png')
    }
    player_image = load_image('player_tank.png')
    enemy_image = load_image('enemy_tank.png')
    MAX_ENEMIES = 5
    MAX_WHOLE = 1
    enemy_spawned = 0
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
    screen.fill((0, 0, 0))
    if level == 1:
        player, level_x, level_y, player2, start_1, start_2 = generate_level(load_level('map.txt'))
    elif level == 2:
        player, level_x, level_y, player2, start_1, start_2 = generate_level(load_level('second lvl.txt'))
    elif level == 3:
        player, level_x, level_y, player2, start_1, start_2 = generate_level(load_level('third lvl.txt'))
    elif level == 4:
        player, level_x, level_y, player2, start_1, start_2 = generate_level(load_level('fourth lvl.txt'))
    elif level == 5:
        player, level_x, level_y, player2, start_1, start_2 = generate_level(load_level('fifth lvl.txt'))
    else:
        return 0
    clock = pygame.time.Clock()
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    last1 = 1
    last2 = 1
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
                    if not player.cool_down and not player.is_Dead:
                        Bullet(player.rect.x, player.rect.y, direction, 1)
                        shot = load_sound('shot.wav')
                        shot.play()
                        player.cool_down = True
                if keys[pygame.K_RIGHT] and not player.is_Dead:
                    move_right = True
                if keys[pygame.K_LEFT] and not player.is_Dead:
                    move_left = True
                if keys[pygame.K_UP] and not player.is_Dead:
                    move_up = True
                if keys[pygame.K_DOWN] and not player.is_Dead:
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
                    if pygame.joystick.Joystick(0).get_axis(0) > 0.5 and not player2.is_Dead:
                        move_right2 = True
                    elif pygame.joystick.Joystick(0).get_axis(0) < -0.5 and not player2.is_Dead:
                        move_left2 = True
                    else:
                        move_left2 = False
                        move_right2 = False
                    if pygame.joystick.Joystick(0).get_axis(1) > 0.5 and not player2.is_Dead:
                        move_down2 = True
                    elif pygame.joystick.Joystick(0).get_axis(1) < -0.5 and not player2.is_Dead:
                        move_up2 = True
                    else:
                        move_up2 = False
                        move_down2 = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    if pygame.joystick.Joystick(0).get_button(1) and not player2.is_Dead:
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
        if move_right and 'right' not in player.update():
            player.rect.x += 4
            player.image = pygame.transform.rotate(player_image, -90)
            direction = 'right'
        elif move_left and 'left' not in player.update():
            player.rect.x -= 4
            player.image = pygame.transform.rotate(player_image, 90)
            direction = 'left'
        elif move_up and 'up' not in player.update():
            player.rect.y -= 4
            player.image = player_image
            direction = 'up'
        elif move_down and 'down' not in player.update():
            player.rect.y += 4
            player.image = pygame.transform.rotate(player_image, 180)
            direction = 'down'
        if coop:
            if move_right2 and 'right' not in player2.update():
                player2.rect.x += 4
                player2.image = pygame.transform.rotate(player_image, -90)
                direction2 = 'right'
            elif move_left2 and 'left' not in player2.update():
                player2.rect.x -= 4
                player2.image = pygame.transform.rotate(player_image, 90)
                direction2 = 'left'
            elif move_up2 and 'up' not in player2.update():
                player2.rect.y -= 4
                player2.image = player_image
                direction2 = 'up'
            elif move_down2 and 'down' not in player2.update():
                player2.rect.y += 4
                player2.image = pygame.transform.rotate(player_image, 180)
                direction2 = 'down'
        if coop:
            if player.kills + player2.kills >= MAX_WHOLE:
                move.stop()
                level += 1
                victory(2, level)
        else:
            if player.kills >= MAX_WHOLE:
                level += 1
                victory(1, level)
        cooldown1 = 5000
        now1 = pygame.time.get_ticks()
        print(len(enemy_group))
        if now1 - last1 >= cooldown1 and len(enemy_group) < MAX_ENEMIES and enemy_spawned <= MAX_WHOLE:
            last1 = now1
            if random.randint(1, 2) == 1:
                Enemy(1, 0, 1)
            else:
                Enemy(12, 0, 2)
            enemy_spawned += 1
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        enemy_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
FPS = 30
size = width, height = 816, 624
screen = pygame.display.set_mode(size)
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
pygame.event.pump()
