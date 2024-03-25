import pygame
import random


TICKRATE = 60
WIDTH = 2560
HEIGHT = 1020
BG = pygame.transform.scale(
    pygame.image.load('pikcer/spais.jpg'),
    (WIDTH , HEIGHT))
RED = (255 , 0 , 0) #игрок
GREEN = (0, 225 , 0) #враг
WHITE= (255,255,255) #текст
VIOLET = (139 , 0 , 255) #елитный боец
BLUE = (66 , 170 , 255) #сапорт
CYANTH = (0 , 255 ,255) #босс
pygame.init()

pygame.mixer.music.load('music/music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

window = pygame.display.set_mode((WIDTH , HEIGHT))

clock = pygame.time.Clock()

class GameManager():
    def __init__(self):
        self.state = 'play'

        self.score = 0 

        self.score_font = pygame.font.Font(None, 45)
        self.score_text = self.score_font.render('0', True , WHITE)



        self.restart_font = pygame.font.Font(None, 55)
        self.restart_text = self.restart_font.render('Press F', True , WHITE)

   
    def draw_score(self):
        window.blit(self.score_text,(10 , 10))

    def update_score(self):
        self.score_text = self.score_font.render(str(self.score), True , WHITE)
    
    def draw_restart(self):
        x= WIDTH // 2 - self.restart_text.get_width() // 2
        y= HEIGHT // 2 - self.restart_text.get_height() // 2
        window.blit(self.restart_text , (x , y))


    def restart(self):
        self.state = 'play'
        self.score = 0
        self.update_score()
        enemis.empty()
        player_lasers.empty()
        enemis_lasers.empty()
        player.hp = 5
        player.rect.center = (WIDTH // 2 , HEIGHT // 2)
        player.hp_bar = pygame.Surface((player.hp * 40 , 10))
        player.hp_bar.fill(RED)
    



class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x , y , img , speed=5 , shoot_cd = TICKRATE):
        super().__init__()
        self.hp = 5
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(center = (x , y))
        self.speed = speed
        self.shoot_cd = Cooldown(shoot_cd)
        self.shoot_sound = pygame.mixer.Sound('music/laser.mp3')
        self.shoot_sound.set_volume(0.2)


    def draw(self):
        window.blit(self.image , self.rect)
    

class Player(Spaceship):
    def __init__(self, x, y, img, speed=5, shoot_cd=TICKRATE):
        super().__init__(x, y, img, speed, shoot_cd)
        self.hp_bar_wrapper = pygame.Surface((200,10))
        self.hp_bar_wrapper.fill(WHITE)
        self.hp_bar_wrapper_pos = (WIDTH - 220 , HEIGHT - 30)

        self.hp_bar = pygame.Surface((self.hp * 40 , 10))
        self.hp_bar.fill(RED)
    
    def draw_hp(self):
        window.blit(self.hp_bar_wrapper , self.hp_bar_wrapper_pos)
        window.blit(self.hp_bar , self.hp_bar_wrapper_pos)

    def update_hp_bar(self):
        self.hp_bar = pygame.Surface((self.hp * 40 , 10))
        self.hp_bar.fill(RED)


    def update(self , keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        if self.rect.top <0:
            self.rect.top = 0
        if self.rect.bottom >   HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left <0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.shoot_cd.done(False):
            if keys[pygame.K_SPACE]:
                self.shoot_cd.reset()
                player_lasers.add(
                    Laser(self.rect.left , self.rect.top , RED , -5)
                )
                player_lasers.add(
                    Laser(self.rect.right , self.rect.top , RED , -5)
                )
                self.shoot_sound.play()


        if pygame.sprite.spritecollideany(self , enemis ,  ):
            game.state = 'over'

        shoot = pygame.sprite.spritecollideany(self , enemis_lasers)
        if shoot:
            shoot.kill()
            explosion.add(Explosion(*self.rect.center))
            self.hp -=1
            self.update_hp_bar()
            if self.hp <= 0:
                game.state = 'over'


    #помошник
# class Saport(Spaceship):
#     def __init__(self, x, y, img, speed=5, shoot_cd=TICKRATE , hp = 100):
#         super().__init__(x, y, img, speed, shoot_cd)
#         self.hp = hp 

#     def get_damage(self):
#         self.hp -= 1
#         if self.hp <= 0:
#             self.kill()
    
#     def update_saport(self):
#         self.rect.y -= self.speed
#         if self.rect.top < HEIGHT:
#             self.kill()
#         collided_laser = pygame.sprite.spritecollideany(self , enemis_lasers , elit_enemy_lasers)
#         if collided_laser:
#             collided_laser.kill()
#             self.get_damage()

#         if self.shoot_cd.done():
#             saport_lasers.add(
#                 Laser(self.rect.centerx , self.rect.top, BLUE, 7)
#                     )
#             saport_lasers.add(
#                 Laser(self.rect.left , self.rect.top, BLUE, 6)
#                     )
#             saport_lasers.add(
#                 Laser(self.rect.right , self.rect.top, BLUE, 6)
#                     )










    #обычный враг
class Enemy(Spaceship):

    def __init__(self, x, y, img, speed=5, shoot_cd=TICKRATE , hp = 2):
        super().__init__(x, y, img, speed, shoot_cd)
        self.hp = hp 

    def get_damage(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            explosion.add(Explosion(*self.rect.center))
            game.score += 1
            game.update_score()

    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
        collided_laser = pygame.sprite.spritecollideany(self , player_lasers)
        if collided_laser:
            collided_laser.kill()
            self.get_damage()

        if self.shoot_cd.done():
            enemis_lasers.add(
                Laser(self.rect.centerx , self.rect.bottom, GREEN, 7)
                    )
            enemis_lasers.add(
                Laser(self.rect.left , self.rect.bottom, GREEN, 6)
                    )
            enemis_lasers.add(
                Laser(self.rect.right , self.rect.bottom, GREEN, 6)
                    )
    # улучшеные враги
class Elit_Enemy(Enemy): 

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
            # explosion.add(Explosion(*self.rect.center))


        collided_laser = pygame.sprite.spritecollideany(self , player_lasers)
        if collided_laser:
            collided_laser.kill()
            self.get_damage()

        if self.shoot_cd.done():
            enemis_lasers.add(
                Laser(self.rect.centerx , self.rect.bottom, VIOLET, 7)
                    )
            enemis_lasers.add(
                Laser(self.rect.left , self.rect.bottom, VIOLET, 6)
                    )
            enemis_lasers.add(
                Laser(self.rect.right , self.rect.bottom, VIOLET, 6)
                    )


# class Boss(Spaceship):
#     def __init__(self, x, y, img, speed=5, shoot_cd=TICKRATE , hp = 2000):
#         super().__init__(x, y, img, speed, shoot_cd)
#         self.hp = hp 

#     def get_damage(self):
#         self.hp -= 1
#         if self.hp <= 0:
#             self.kill()
    
#     def update(self):
#         self.rect.y += self.speed
#         if self.rect.top > HEIGHT:
#             self.kill()
#         collided_laser = pygame.sprite.spritecollideany(self , player_lasers)
#         if collided_laser:
#             collided_laser.kill()
#             self.get_damage()

#         if self.shoot_cd.done():
#             enemis_lasers.add(
#                 Laser(self.rect.centerx , self.rect.bottom, CYANTH, 7)
#                     )
#             enemis_lasers.add(
#                 Laser(self.rect.left , self.rect.bottom, CYANTH, 6)
#                     )
#             enemis_lasers.add(
#                 Laser(self.rect.right , self.rect.bottom, CYANTH, 6)
                    # )    



class Laser(pygame.sprite.Sprite):
    def __init__(self , x , y , color , speed):
        super().__init__()
        self.image = pygame.Surface((3, 15))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = speed
    def update(self):
        self.rect.y += self.speed

class Explosion(pygame.sprite.Sprite):
    def __init__(self , x , y , callback = None):
        super().__init__()
        self.callback = callback
        self.frames_count = 12
        self.frames_index = 0
        self.frame_cd = Cooldown(TICKRATE // 10)
        image = pygame.image.load('pikcer/Explosion.png')
        frame_wigth = image.get_width() // self.frames_count
        frame_height = image.get_height() 
        self.rect = (x - frame_wigth // 2 , y - frame_height // 2)
        self.frame = []
        for i in range(self.frames_count):
            self.frame.append(image.subsurface((i * frame_wigth, 0, frame_wigth, frame_height)))
        self.image = self.frame[0]

        sound = pygame.mixer.Sound('music/explosion_music.wav')
        sound.set_volume(0.1)
        sound.play()




    def update(self):
        if self.frame_cd.done():
            self.frames_index += 1
            if self.frames_index == self.frames_count:
                self.kill()
            else:
                self.image = self.frame[self.frames_index]
class Cooldown():
    def __init__(self , ticks):
        self.ticks = ticks
        self.current = ticks

    def reset(self):
        self.current = self.ticks

    def done(self , need_reset = True):
        if self.current == 0:
            if need_reset:
                self.reset()
            return True
        else:
            self.current -= 1
            return False
player = Player(
    WIDTH // 2,
    HEIGHT //2,
    'pikcer/player.png',
    shoot_cd= TICKRATE // 7
)
enemis = pygame.sprite.Group()
enemis_spawn_cd = Cooldown(TICKRATE)

saport = pygame.sprite.Group()
saport_spawn_cd = Cooldown(TICKRATE)

boss = pygame.sprite.Group()



elit_enemy = pygame.sprite.Group()
elit_enemy_spawn_cd = Cooldown(TICKRATE)

player_lasers = pygame.sprite.Group()
saport_lasers = pygame.sprite.Group()
enemis_lasers = pygame.sprite.Group()
elit_enemy_lasers = pygame.sprite.Group()
boss_lasers = pygame.sprite.Group()

explosion = pygame.sprite.Group()

game = GameManager()
while True:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    for e in events:
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_f and game.state == 'over':
                game.restart()
    #обнова
    if game.state == 'play':
        if enemis_spawn_cd.done():
            x = random.randint(50 , WIDTH - 50)
            enemis.add(Enemy( x , -100 , 'pikcer/enemy.png' , 1 , TICKRATE * 2 ))
        if elit_enemy_spawn_cd.done():
            x = random.randint(20, WIDTH - 20 )
            elit_enemy.add(Elit_Enemy(x , -100 , 'pikcer/elit_enemy.png' , 2 , TICKRATE * 2))

        # if saport_spawn_cd.done():
        #     x = random.randint(50, WIDTH - 50 )
        #     saport.add(Saport(x , 600 , 'pikcer/saport.xell.png' , 1 ,TICKRATE * 1))




        player_lasers.update()
        enemis_lasers.update()  
        # elit_enemy_lasers.update()
        saport_lasers.update()
        enemis.update()
        # saport.update()
        # elit_enemy.update()
        player.update(keys)
        explosion.update()
    #отресовка
    window.blit(BG, (0,0))
    game.draw_score()
    player_lasers.draw(window)
    enemis_lasers.draw(window)      
    saport_lasers.draw(window)      
    # elit_enemy_lasers.draw(window)
    # elit_enemy.draw(window)
    # saport.draw(window)
    enemis.draw(window)
    player.draw()
    player.draw_hp()
    explosion.draw(window)
    if game.state == 'over':
        game.draw_restart()

    pygame.display.flip()
    clock.tick(TICKRATE)