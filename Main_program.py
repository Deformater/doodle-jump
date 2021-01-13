import os
import sys
import random
import pygame


# инициализация
pygame.init()
size = width, height = 471, 719
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Doodle jump')
screen.fill((255, 255, 255))

gen_coords = 0  # переменная для определения позиции последней сгенерированной платформы
P_RANDOM = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2]   # массив для выбора типа платформы
MONSTER = ["Monster_1.png", "Monster_2.png", "Monster_3.png", "Monster_4.png"]  # массив с картинками для монстров
clock = pygame.time.Clock()


# функция для загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()

    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()

        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)

    else:
        image = image.convert_alpha()

    return image


# функция для определения наличия монстра на платформе
def monster_random():
    return random.random() > 0.99


# генерация платформ
def generate():
    global gen_coords

    eczemplar = Platform(width // 2, height - 25)
    gen_coords = height - 26

    for i in range(random.randint(14, 18)):
        gen_coords = random.randint(gen_coords - 304 + dude.rect.h + eczemplar.rect.h,
                                    gen_coords - eczemplar.rect.h - 1)
        eczemplar = PLATFORM[random.choice(P_RANDOM)](random.randint(0, width - eczemplar.rect.w), gen_coords)


# класс синей вставки сверху поля
class Vstavka(pygame.sprite.Sprite):
    image = load_image("blue_vstavka.png")

    def __init__(self):
        super().__init__(all_sprites)

        self.image = Vstavka.image
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.score = Score()
        self.pause = Pause()

        self.rect.x = 0
        self.rect.y = 0


# класс значка паузы
class Pause(pygame.sprite.Sprite):
    image = load_image("pause1.png")

    def __init__(self):
        super().__init__(all_sprites)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = width - 50
        self.rect.y = 10

    def update(self, *args):
        if args and args[0].pos[0] in range(self.rect.x, self.rect.x + self.rect.w)\
                and args[0].pos[1] in range(self.rect.y, self.rect.y + self.rect.h):
            pause_screen()


# класс результата(высоты подъёма)
class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(dezign)

        self.myFont = pygame.font.Font('DoodleJump.ttf', 30)
        self.myFont.bold = True
        self.fontImage = self.myFont.render(str(0), True, (0, 0, 0))
        screen.blit(self.fontImage, (10, 5))

        self.score = 0

    def update(self, *args):
        self.fontImage = self.myFont.render(str(camera.moving), True, (0, 0, 0))
        self.score = camera.moving
        screen.blit(self.fontImage, (10, 5))


# класс камеры
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dy = height
        self.delta = 0
        self.moving = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.y += 1

    # позиционировать камеру на объекте target
    def update(self, target):
        i = 0
        self.delta = target.delta - 324

        while i < target.delta - 324:
            for sprite in platforms:
                camera.apply(sprite)
            camera.apply(dude)
            i += 1
            self.moving += 1


# класс заднего фона
class Background(pygame.sprite.Sprite):
    image = load_image("background.png")

    def __init__(self):
        super().__init__(all_sprites)

        self.image = Background.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = 0
        self.rect.y = 0


# класс монстров
class Monster(pygame.sprite.Sprite):

    def __init__(self, platform):
        super().__init__(monsters)

        image = load_image(random.choice(MONSTER), -1)  # выбор изображения для монстра
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.platform = platform

        self.rect.x = self.platform.rect.x
        self.rect.y = self.platform.rect.y - self.rect.h

    def update(self, *args):
        self.rect.x = self.platform.rect.x
        self.rect.y = self.platform.rect.y - self.rect.h

        if pygame.sprite.spritecollideany(self, shells):
            monsters.remove(self)
            self.platform.monster = None
            self.platform = None
            del self


# класс "классической" платформы
class Platform(pygame.sprite.Sprite):
    image = load_image("platform_classic.png")

    def __init__(self, x, y):
        super().__init__(platforms)
        self.image = Platform.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.monster = None

        self.rect.x = x
        self.rect.y = y

    def update(self, arg=False):
        global gen_coords
        if not arg:
            if self.rect.y > height:
                all_sprites.remove(self.monster)
                gen_coords = random.randint(gen_coords - 304 + dude.rect.h + self.rect.h, gen_coords - self.rect.h - 1)
                self.rect.x, self.rect.y = random.randint(0, width - self.rect.w), gen_coords

                if monster_random() and self.monster is None:
                    self.monster = Monster(self)
        else:
            dude.spring = False


# класс ломающейся платформы
class PlatformCrush(Platform):
    image = load_image("platform_crush.png")

    def __init__(self, x_coords, y_coords):
        super().__init__(x_coords, y_coords)

        self.image = PlatformCrush.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, arg=False):
        global gen_coords
        if not arg:
            if self.rect.y > height:
                gen_coords = random.randint(gen_coords - 304 + dude.rect.h + self.rect.h, gen_coords - self.rect.h - 1)
                self.rect.x, self.rect.y = random.randint(0, width - self.rect.w), gen_coords
        else:
            platforms.remove(self)
            del self


# класс платформы с пружиной
class PlatformSpring(Platform):
    image = load_image("platform_spring.png")

    def __init__(self, x, y):
        super().__init__(x, y)

        self.image = PlatformSpring.image
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, arg=False):
        global gen_coords
        if not arg:
            if self.rect.y > height:
                gen_coords = random.randint(gen_coords - 304 + dude.rect.h + self.rect.h, gen_coords - self.rect.h - 1)
                self.rect.x, self.rect.y = random.randint(0, width - self.rect.w), gen_coords
        else:
            dude.vertikal_speed = -30
            dude.spring = True


# класс подвижной платформы
class PlatformMove(Platform):
    image = load_image("platform_moving.png")

    def __init__(self, x, y):
        super().__init__(x, y)

        self.image = PlatformMove.image
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = 3
        self.monster = None

    def update(self, arg=False):
        global gen_coords
        if not arg:
            if self.rect.y > height:
                all_sprites.remove(self.monster)
                gen_coords = random.randint(gen_coords - 304 + dude.rect.h + self.rect.h, gen_coords - self.rect.h - 1)
                self.rect.x, self.rect.y = random.randint(0, width - self.rect.w), gen_coords

                if monster_random() and self.monster is None:
                    self.monster = Monster(self)

            if self.rect.x + self.rect[2] >= width:
                self.speed = -3

            if self.rect.x <= 0:
                self.speed = 3

            self.rect.x += self.speed
        else:
            dude.spring = False


# класс снаряда
class Shell(pygame.sprite.Sprite):
    image = load_image('shell.png')

    def __init__(self, event):
        super().__init__(shells)
        self.image = Shell.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = dude.rect.x + dude.rect[2] // 2 - self.rect.w
        self.rect.y = dude.rect.y

        self.new_x, self.new_y = event[0] - self.rect.w // 2, event[1] - self.rect.h // 2
        self.old_x, self.old_y = self.rect.x, self.rect.y

        if not (self.old_x == self.new_x):  # вычисление прямой движения снаряда
            self.xy = lambda x: ((self.new_y - self.old_y) * x - self.old_x * (self.new_y - self.old_y) + self.old_y *
                                 (self.new_x - self.old_x)) / (self.new_x - self.old_x)
        else:
            self.xy = lambda x: x + 10

        self.a = (self.new_y - self.old_y) ** 2 + (self.new_x - self.old_x) ** 2
        self.b = self.new_y - self.old_y
        self.c = self.new_x - self.old_x
        self.cos = self.c / self.a ** 0.5

    def update(self, *args):
        if (-0.5 < self.cos < 0.5) and (self.new_y < self.old_y):
            if abs(self.cos) > 0.1:
                self.rect.x += 30 * self.cos
                self.rect.y = self.xy(self.rect.x)
            else:
                self.rect.y -= 30

            if not(0 < self.rect.y < height and 0 < self.rect.x < width):
                shells.remove(self)
                del self
        else:
            shells.remove(self)
            del self


# класс главного пресонажа
class Doodle(pygame.sprite.Sprite):
    image = load_image("doodle.jpeg", -1)

    def __init__(self):
        super().__init__(all_sprites)

        self.image = Doodle.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = width // 2
        self.rect.y = height - 25 - self.rect.h
        self.y = height - 10

        self.vertikal_speed = -14
        self.horizontal_speed = 4
        self.delta = 0
        self.a1 = 0.5
        self.a2 = 0.3

        self.flipness = 0
        self.spring = False
        self.motion = None

    def update(self, *args):
        global gen_coords

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:  # выстрел
            self.shoot(args[0].pos)

        if args and args[0].type == pygame.KEYDOWN:  # горизонтальное движение
            if args[0].key == 97:
                self.motion = 'A'
            if args[0].key == 100:
                self.motion = 'D'

        if args and args[0].type == pygame.KEYUP:   # горизонтальное движение
            if args[0].key == 97 and self.motion == 'A':
                self.motion = None
            if args[0].key == 100 and self.motion == 'D':
                self.motion = None
            self.horizontal_speed = 2

        if self.motion is not None:  # горизонтальное движение
            self.movement_horizontal(self.motion)

        if pygame.sprite.spritecollideany(self, platforms):  # пересечение с платформами
            if self.vertikal_speed > 0:
                if pygame.sprite.spritecollideany(self, platforms).__class__.__name__ != 'PlatformCrush':
                    self.vertikal_speed = -14
                pygame.sprite.spritecollideany(self, platforms).update(True)

        if pygame.sprite.spritecollideany(self, monsters):  # пересечение с монстрами
            if not self.spring:
                self.kill()
            else:
                monsters.remove(pygame.sprite.spritecollideany(self, monsters))

        if self.rect.y > height:    # выход за пределы поля
            self.kill()

        if camera.dy - self.rect.y > 324:   # движение камеры
            self.delta = camera.dy - self.rect.y
            camera.update(self)
            gen_coords += camera.delta
        self.movement_vertical()    # вертикальное движение

    def movement_vertical(self):    # вертикальное движение
        self.rect.y += self.vertikal_speed
        self.vertikal_speed += self.a1

    def movement_horizontal(self, motion):  # горизонтальное движение
        if motion == 'A':
            self.rect.x -= self.horizontal_speed
            if self.rect.x + self.rect.w < 0:
                self.rect.x = width
            self.image = pygame.transform.flip(self.image, self.flipness != 0, False)
            self.flipness = 0

        if motion == 'D':
            self.rect.x += self.horizontal_speed
            if self.rect.x > width:
                self.rect.x = 0 - self.rect.w
            self.image = pygame.transform.flip(self.image, self.flipness != 1, False)
            self.flipness = 1

        self.horizontal_speed += self.a2

    def shoot(self, pos):   # выстрел
        Shell(pos)

    def kill(self):  # смерть
        all_sprites.remove(self)
        death_screen()


# инициализация текста для стартогого экрана
def start_text_init():
    intro_text = ["Doodle jump",
                  "григорий муравенко",
                  "Click to start"]
    font = pygame.font.Font('DoodleJump.ttf', 30)
    font.bold = True

    string_rendered = font.render(intro_text[0], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 35
    intro_rect.x = 35
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render(intro_text[2], True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 600
    intro_rect.x = (width - intro_rect.w) // 2
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font('Bradley Hand.ttf', 20)
    string_rendered = font.render(intro_text[1], True, pygame.Color('red'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 65
    intro_rect.x = 35
    screen.blit(string_rendered, intro_rect)


# начальный экран
def start_screen():
    generate()

    # отрисовка
    all_sprites.draw(screen)
    platforms.draw(screen)

    # инициализация текста
    start_text_init()

    while True:
        # обработка внешних событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        pygame.display.flip()
        clock.tick(60)


# инициализация текста для экрана паузы
def pause_text_init():
    intro_text = ["Click to continue"]
    font = pygame.font.Font('DoodleJump.ttf', 30)
    font.bold = True
    string_rendered = font.render(intro_text[0], True, pygame.Color('black'))

    intro_rect = string_rendered.get_rect()
    intro_rect.y = 600
    intro_rect.x = (width - intro_rect.w) // 2
    screen.blit(string_rendered, intro_rect)


# экран паузы
def pause_screen():
    # инициализация текста
    pause_text_init()

    while True:
        # обработка внешних событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # продолжаем игру

        pygame.display.flip()
        clock.tick(60)


# инициализация текста для экрана смерти
def death_text_init(s):
    intro_text = ['You died', 'your best score: ' + str(s),
                  'your score: ' + str(vstavka.score.score),
                  "Click to restart"]
    font = pygame.font.Font('DoodleJump.ttf', 30)
    font.bold = True

    string_rendered1 = font.render(intro_text[0], True, pygame.Color('red'))
    intro_rect1 = string_rendered1.get_rect()
    intro_rect1.y = 35
    intro_rect1.x = 35
    screen.blit(string_rendered1, intro_rect1)

    string_rendered2 = font.render(intro_text[1], True, pygame.Color('black'))
    intro_rect2 = string_rendered2.get_rect()
    intro_rect2.y = 65
    intro_rect2.x = 35
    screen.blit(string_rendered2, intro_rect2)

    string_rendered3 = font.render(intro_text[2], True, pygame.Color('black'))
    intro_rect3 = string_rendered3.get_rect()
    intro_rect3.y = 95
    intro_rect3.x = 35
    screen.blit(string_rendered3, intro_rect3)

    string_rendered4 = font.render(intro_text[3], True, pygame.Color('black'))
    intro_rect4 = string_rendered4.get_rect()
    intro_rect4.y = 600
    intro_rect4.x = (width - intro_rect4.w) // 2
    screen.blit(string_rendered4, intro_rect4)

    return (string_rendered1, intro_rect1), (string_rendered2, intro_rect2),\
           (string_rendered3, intro_rect3), (string_rendered4, intro_rect4)


# занесение и чтение файла со счётом
def score_save():
    f = open('BestScore.txt', 'r', encoding="utf-8")
    s = int(f.readline())
    if s < vstavka.score.score:
        s = vstavka.score.score
    f.close()
    f = open('BestScore.txt', 'w', encoding="utf-8")
    f.write(str(s))
    f.close()
    return s


# экран конца игры
def death_screen():
    # занесение конечного результата в файл
    s = score_save()

    # инициализация текста
    text = death_text_init(s)
    string_rendered1, intro_rect1 = text[0]
    string_rendered2, intro_rect2 = text[1]
    string_rendered3, intro_rect3 = text[2]
    string_rendered4, intro_rect4 = text[3]

    # удаление голубой вставки
    all_sprites.remove(vstavka.pause)
    all_sprites.remove(vstavka)
    while True:
        # обработка внешних событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                os.execl(sys.executable, sys.executable, *sys.argv)

        # отрисовка и обновление всех групп спрайтов
        all_sprites.draw(screen)
        platforms.draw(screen)
        monsters.draw(screen)
        monsters.update()
        platforms.update()
        all_sprites.update()

        # отрисовка текста
        screen.blit(string_rendered1, intro_rect1)
        screen.blit(string_rendered2, intro_rect2)
        screen.blit(string_rendered3, intro_rect3)
        screen.blit(string_rendered4, intro_rect4)

        clock.tick(60)
        pygame.display.flip()


# основной цикл
if __name__ == '__main__':
    PLATFORM = [Platform, PlatformMove, PlatformSpring, PlatformCrush]  # массив для выбора типа платформ

    # изменение иконки
    icon = load_image("icon.png")
    pygame.display.set_icon(icon)

    # создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    shells = pygame.sprite.Group()
    dezign = pygame.sprite.Group()

    Background()
    dude = Doodle()
    start_screen()  # начальная заставка
    camera = Camera()  # создание камеры
    vstavka = Vstavka()  # создание вставки

    #   основной цикл
    running = True
    while running:
        # обработка внешних событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button in [1, 2, 3]):
                vstavka.pause.update(event)
                dude.update(event)
            elif event.type == pygame.KEYDOWN:
                dude.update(event)
            elif event.type == pygame.KEYUP:
                if event.key in [97, 100]:
                    dude.update(event)

        # отрисовка и обновление всех групп спрайтов
        all_sprites.draw(screen)
        platforms.draw(screen)
        monsters.draw(screen)
        monsters.update()
        platforms.update()
        all_sprites.update()
        dezign.update()
        shells.draw(screen)
        shells.update()

        clock.tick(60)
        pygame.display.flip()
