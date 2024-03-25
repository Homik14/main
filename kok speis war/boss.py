import pygame
import random

WIDTH  = 1600
HEIGHT =  800
FPS    =   60

# Задаем цвета
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)

# переменные 
timer_games = 0
timer_stats = 0
u = 100
boss_life = 100
player_ship_life = 100

#разное 
# pygame.time.set_timer(pygame.USEREVENT, 1000)     # таймер , смотреть инструкцию


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 60))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(600,900)
        self.rect.y = random.randrange(HEIGHT - 700)
        self.speedx = random.randrange(-10 , 10)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speedx = random.randrange(-10 ,-1)
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = random.randrange(1 , 10)

    def draw_boss(self, surf, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH_1 = 150
        BAR_HEIGHT_1 = 20
        fill_1 = (pct / 100) * BAR_LENGTH_1
        outline_rect_1 = pygame.Rect(self.rect.x-70/2, self.rect.y-25, BAR_LENGTH_1, BAR_HEIGHT_1)
        fill_rect_1 = pygame.Rect(self.rect.x-70/2, self.rect.y-25, fill_1, BAR_HEIGHT_1)
        pygame.draw.rect(surf, GREEN, fill_rect_1)
        pygame.draw.rect(surf, WHITE, outline_rect_1, 2)






all_sprites = pygame.sprite.Group()
all_sprites_1 = pygame.sprite.Group()
mobs = pygame.sprite.Group()

boss = Boss()
all_sprites_1.add(boss)
mobs1 = pygame.sprite.Group()




running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():         # запускает таймер ,каждую секунду он считает
        if e.type == pygame.USEREVENT:   # только в его границах работает таймер 
            timer_games += 1



        if e.type == pygame.QUIT:
            running = False 
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()
    all_sprites_1.update()


    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    all_sprites_1.draw(screen)
    boss.draw_boss(screen, boss_life)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()