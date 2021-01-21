import pygame
import math
import random
import time

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
        self.health = 10
        self.powerups = [False, False, False]

    def move(self, event):
        global running
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
        for wall in pygame.sprite.spritecollide(self, wallgroup, False):
            if self.rect.right in range(wall.rect.left, wall.rect.centerx) or self.rect.left in range(wall.rect.centerx, wall.rect.right):
                self.rect.centerx += -(self.xspeed*1.1)
                self.xspeed = 0
            if self.rect.top in range(wall.rect.centery, wall.rect.bottom) or self.rect.bottom in range(wall.rect.top, wall.rect.centery):
                self.rect.centery += -(self.yspeed*1.1)
                self.yspeed = 0
        self.xspeed += -self.xspeed*0.01
        self.yspeed += -self.yspeed*0.01
        self.rect.move_ip(self.xspeed, self.yspeed)
        self.mousex, self.mousey = pygame.mouse.get_pos()
        self.angle = math.atan2((self.rect.x+16)-self.mousex, (self.rect.y+16)-self.mousey)
        self.image = pygame.transform.rotate(self.og_img, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
        if self.powerups[0]:
            self.health += 5
            self.powerups[0] = False
        self.healthtext = "♥"*self.health
        self.healthbar = mainfont.render(self.healthtext, True, (255, 0, 0))
        self.healthrect = self.healthbar.get_rect(center=(self.rect.centerx, self.rect.centery-20))
        display.blit(self.healthbar, self.healthrect)
        if self.health <= 0:
            playergroup.remove(self)
            explode.play()
            time.sleep(1)
            running = False

class Bullet(pygame.sprite.Sprite):

    def __init__(self, target, pos, good=True, offset=False):
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
        if offset:
            self.rect.move_ip(self.yc*4, self.xc*4)
    
    def update(self):
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
                enemy.health += -1
        for wall in wallgroup:
            if self.rect.colliderect(wall):
                bulletgroup.remove(self)
                wallgroup.update()
                wall.damage += 1
        if not self.good and self.rect.colliderect(player):
            bulletgroup.remove(self)
            if player.powerups[1]:
                player.health += 0
            else:
                player.health += -1

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
        self.health = 10
    
    def update(self):
        self.targetx, self.targety = player.rect.center
        self.angle = math.atan2((self.rect.centerx)-self.targetx, (self.rect.centery)-self.targety)
        self.image = pygame.transform.rotate(self.og_img, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.timer += 1
        if self.timer == 600:
            self.timer = 0
            bulletgroup.add(Bullet(player.rect.center, self.rect.center, good=False))
            shoot.play()
        self.healthtext = "♥"*self.health
        self.healthbar = mainfont.render(self.healthtext, True, (255, 0, 0))
        self.healthrect = self.healthbar.get_rect(center=(self.rect.centerx, self.rect.centery-20))
        display.blit(self.healthbar, self.healthrect)
        if self.health <= 0:
            enemygroup.remove(self)
            explode.play()
            powergroup.add(Powerup(random.randint(0, 2), self.rect.center))


class Wall(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("textures/wall0.png")
        self.image.set_colorkey((255, 255, 255))
        self.length = random.randint(1, 4)*64
        self.rotation = random.randint(-1, 2)*90
        self.rect = self.image.get_rect(center=pos)
        self.damage = 0

    def update(self):
        if self.damage > 5:
            wallgroup.remove(self)
            explode.play()
            return
        self.image = pygame.image.load(f"textures/wall{self.damage}.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (self.length, 16))
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

class Powerup(pygame.sprite.Sprite):

    def __init__(self, power, pos):
        super().__init__()
        self.power = power
        self.image = pygame.image.load(f"textures/powerup{self.power}.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(center=pos)
    
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            player.powerups[self.power] = True
            powergroup.remove(self)

#initializing display
SHEIGHT = 720
SWIDTH = 1024
pygame.init()
display = pygame.display.set_mode((SWIDTH, SHEIGHT))
version = 0.4
pygame.display.set_caption(f"Kaboom {version}")
mainfont = pygame.font.Font("font/arial.ttf", 24)
#initializing sound
pygame.mixer.init()
shoot = pygame.mixer.Sound("sounds/shot.mp3")
explode = pygame.mixer.Sound("sounds/explosion.mp3")
#initializing sprites
player = Player()
playergroup = pygame.sprite.GroupSingle()
bulletgroup = pygame.sprite.Group()
enemygroup = pygame.sprite.Group()
wallgroup = pygame.sprite.Group()
powergroup = pygame.sprite.Group()
playergroup.add(player)
for enemy in range(random.randint(2, 5)):
    enemygroup.add(Enemy((random.randint(0, SWIDTH), random.randint(0, SHEIGHT))))
for wall in range(random.randint(3, 10)):
    wallgroup.add(Wall((random.randint(0, SWIDTH), random.randint(0, SHEIGHT))))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bulletgroup.add(Bullet(pygame.mouse.get_pos(), player.rect.center))
                shoot.play()
                if player.powerups[2]:
                    print("machine gun")
                    bulletgroup.add(Bullet(pygame.mouse.get_pos(), player.rect.center, offset=True))
                    shoot.play()
    display.fill((0, 127, 255))
    playergroup.draw(display)
    bulletgroup.draw(display)
    enemygroup.draw(display)
    wallgroup.draw(display)
    powergroup.draw(display)
    player.move(pygame.key.get_pressed())
    bulletgroup.update()
    enemygroup.update()
    wallgroup.update()
    powergroup.update()
    pygame.display.flip()
pygame.quit()