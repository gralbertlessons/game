import pygame
import os

''' Переменные '''
worldx = 960
worldy = 720

fps = 40

ani = 7

BLUE = (25, 25, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ALPHA = (120, 211, 237)
ALPHA2 = (12, 211, 240)
ALPHA3 = (0, 255, 222)

PL_WIDTH = 32
PL_HEIGHT = 32
PL_COLOR = "#84c3be"


''' Объекты '''
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.health = 10
        self.on_platform = False

        self.images = []
        for i in range(1, 9):
            img = pygame.image.load(os.path.join('images', 'hero' + str(i) + '.png'))
            img.convert_alpha()
            img.set_colorkey(ALPHA)
            self.images.append(img)
            self.image = self.images[0]
            self.rect = self.image.get_rect()

    def control(self, x, y):
        self.movex += x
        self.movey += y

    def jump(self):
        hit_ground = pygame.sprite.spritecollide(self, ground_list, False)
        if hit_ground or self.on_platform:
            self.movey -= 35

    def update(self):
        self.rect.x += self.movex
        self.rect.y += self.movey

        # Двигаемся влево
        if self.movex < 0:
            if self.rect.x < 0:
                self.rect.x += 50
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # Двигаемся вправо
        if self.movex > 0:
            if self.rect.x > worldx - 15:
                self.rect.x -= 50
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]

        hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for item in hit_list:
            if self.movex < 0:
                self.rect.x += 75
            if self.movex > 0:
                self.rect.x -= 75
            if self.health > 0:
                self.health -= 1
            print(self.health)
            if self.health < 0:
                break

        hit_list2 = pygame.sprite.spritecollide(self, ground_list, False)
        for item in hit_list2:
            self.movey = -3

        self.on_platform = False

        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                self.on_platform = True
                if self.movey > 0:
                    self.rect.bottom = p.rect.top
                    self.movey = 0

    def gravity(self):
        self.movey += 3


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def move(self):
        speed = 3

        if self.counter >=0 and self.counter <= 80:
            self.rect.x += speed
        elif self.counter >= 80 and self.counter <= 160:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1


class Level ():
    @staticmethod
    def level(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1], 'enemy.png')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            print("Level " + str(lvl))

        return enemy_list

    @staticmethod
    def ground(lvl, x, y, w, h):
        ground_list = pygame.sprite.Group()
        if lvl == 1:
            ground = Platform(x, y, w, h, 'block-ground.png')
            ground_list.add(ground)
        if lvl == 2:
            print("Level " + str(lvl))
        return ground_list


class Platform(pygame.sprite.Sprite):
    def __init__(self, locx, locy, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA3)
        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy


class Pl(pygame.sprite.Sprite):
    def __init__(self, locx, locy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('images', 'block.jpg'))
        self.rect = self.image.get_rect()
        self.rect.x = locx
        self.rect.y = locy


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


''' Настройки '''
world = pygame.display.set_mode([worldx, worldy])
backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
clock = pygame.time.Clock()
pygame.init()
backdropbox = world.get_rect()
main = True

ground_list = Level.ground(1, 0, worldy-53, 960, 53)

player = Player()

y = 500


player.rect.x = 0
y += 50
player.rect.y = y

player_list = pygame.sprite.Group()
player_list.add(player)

steps = 10

eloc = [300, 600]
enemy_list = Level.level(1, eloc)

pygame.font.init()
font1 = pygame.font.Font(None, 48)
text1 = font1.render("Конец игры!", True, BLACK)

pl_group = pygame.sprite.Group()
platforms = []

level = []
with open("level.txt", "r") as f:
    for line in f:
        level.append(line.replace("\n", "")
                     .replace("\"", "")
                     .replace(",", ""))


x = 0
y = 0
for row in level:
    for item in row:
        if item == "_":
            pf = Pl(x, y)
            pl_group.add(pf)
            platforms.append(pf)

            # pf = pygame.Surface((PL_WIDTH, PL_HEIGHT))
            # pf.fill(pygame.Color(PL_COLOR))
            # world.blit(pf, (x, y))
        x += PL_WIDTH
    y += PL_HEIGHT
    x = 0


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera

    l, t = -l + worldx / 2, -t + worldy / 2

    l = min(0, l)
    l = max(-(camera.width - worldx), l)
    t = max(-(camera.height - worldy), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)

total_level_width = worldx + 500
total_level_height = worldy

camera = Camera(camera_configure, total_level_width, total_level_height)

''' Основной цикл игры '''
while main:
    world.blit(backdrop, backdropbox)

    player.gravity()
    player.update()
    #pl_group.draw(world)
    #ground_list.draw(world)
    #enemy_list.draw(world)
    #player_list.draw(world)

    camera.update(player)

    for i in [pl_group, ground_list, enemy_list, player_list]:
        for e in i:
            world.blit(e.image, camera.apply(e))

    for enemy in enemy_list:
        enemy.move()

    ''' Блок "Конец игры" начало'''
    if player.health == 0:
        world.blit(text1, (10, 100))

    if player.health < 0:
        world.blit(text1, (10, 100))

    ''' Блок "Конец игры" конец'''

    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps, 0)

            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)

            if event.key == pygame.K_UP or event.key == ord('w'):
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)
