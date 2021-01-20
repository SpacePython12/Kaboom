import pygame
import math
import random

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("textures/player.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.og_img = self.image
        self.og_img.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(width=32, height=32)
        self.rect.centerx = int(SWIDTH/2)
        self.rect.centery = int(SHEIGHT/2)
        self.xspeed = 0
        self.yspeed = 0

    def move(self, event):
        if event[pygame.K_w]:
            self.yspeed += -0.1
        if event[pygame.K_s]:
            self.yspeed += 0.1
        if event[pygame.K_a]:
            self.xspeed += -0.1
        if event[pygame.K_d]:
            self.xspeed += 0.1
        if self.rect.top <= 0:
            self.rect.bottom = SHEIGHT-1
        if self.rect.bottom >= SHEIGHT:
            self.rect.top = 1
        if self.rect.left <= 0:
            self.rect.right = SWIDTH-1
        if self.rect.right >= SWIDTH:
            self.rect.left = 1
        self.xspeed += -self.xspeed*0.01
        self.yspeed += -self.yspeed*0.01
        self.rect.move_ip(self.xspeed, self.yspeed)
        self.mousex, self.mousey = pygame.mouse.get_pos()
        self.angle = math.atan2((self.rect.x+16)-self.mousex, (self.rect.y+16)-self.mousey)
        self.image = pygame.transform.rotate(self.og_img, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, target, pos, good=True):
        super().__init__()
        self.image = pygame.image.load("textures/bullet.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (12, 21))
        self.rect = self.image.get_rect(width=12, height=21)
        self.rect.center = pos
        self.angle = math.atan2(self.rect.centerx-target[0], self.rect.centery-target[1])
        self.image = pygame.transform.rotate(self.image, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.xc = math.cos(self.angle)*8
        self.yc = math.sin(self.angle)*8
        self.good = good
    
    def update(self):
        global running
        self.rect.move_ip(-self.yc, -self.xc)
        if self.rect.top <= 0:
            self.kill
        if self.rect.bottom >= SHEIGHT:
            self.kill
        if self.rect.left <= 0:
            self.kill
        if self.rect.right <= SWIDTH:
            self.kill
        for enemy in enemygroup:
            if self.good and self.rect.colliderect(enemy):
                bulletgroup.remove(self)
                enemygroup.remove(enemy)
                print("enemy")
        if not self.good and self.rect.colliderect(player):
            bulletgroup.remove(self)
            playergroup.remove(player)
            running = False
            print("player")

class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("textures/enemy.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.og_img = self.image
        self.og_img.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(width=32, height=32)
        self.rect.center = pos
        self.xspeed = 0
        self.yspeed = 0
        self.timer = random.randint(0, 300)
    
    def update(self):
        self.targetx, self.targety = player.rect.center
        self.angle = math.atan2((self.rect.centerx)-self.targetx, (self.rect.centery)-self.targety)
        self.image = pygame.transform.rotate(self.og_img, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.timer += 1
        if self.timer == 300:
            self.timer = 0
            bulletgroup.add(Bullet(player.rect.center, self.rect.center, good=False))


#initializing display
SHEIGHT = 720
SWIDTH = 1024
pygame.init()
display = pygame.display.set_mode((SWIDTH, SHEIGHT))
version = f"Alpha 0.0.2"
pygame.display.set_caption(f"Kaboom {version}")
#initializing sprites
player = Player()
playergroup = pygame.sprite.GroupSingle()
bulletgroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
playergroup.add(player)
for enemy in range(random.randint(2, 5)):
    enemygroup.add(Enemy((random.randint(0, SWIDTH), random.randint(0, SHEIGHT))))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[pygame.BUTTON_LEFT-1] and event.type == pygame.MOUSEBUTTONDOWN:
            bulletgroup.add(Bullet(pygame.mouse.get_pos(), player.rect.center))
    display.fill((0, 127, 255))
    playergroup.draw(display)
    bulletgroup.draw(display)
    enemygroup.draw(display)
    player.move(pygame.key.get_pressed())
    bulletgroup.update()
    enemygroup.update()
    pygame.display.flip()
pygame.quit()