import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


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


def game():
    direction = 'up'

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

        def update(self):
            for i in tiles_group:
                if str(i.tile_type) == 'wall' and pygame.sprite.collide_mask(self, i):
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
        def __init__(self, x, y, direct):
            super().__init__(all_sprites)
            self.direction = direction
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
                    Tile('empty_small', i.x, i.y)
                    i.kill()
            if self.rect.y < -10:
                self.kill()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('empty', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y

    tile_images = {
        'wall': load_image('brick2.png'),
        'empty': load_image('empty.png'),
        'empty_small': load_image('empty_small.png')
    }
    player_image = load_image('player_tank.png')

    tile_width, tile_height = 48, 24
    # основной персонаж
    player = None

    # группы спрайтов
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()

    player, level_x, level_y = generate_level(load_level('map.txt'))
    clock = pygame.time.Clock()
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    Bullet(player.rect.x, player.rect.y, direction)
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

        all_sprites.draw(screen)
        all_sprites.update()
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
FPS = 30
size = width, height = 816, 624
screen = pygame.display.set_mode(size)
