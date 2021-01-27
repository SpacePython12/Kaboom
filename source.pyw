import pygame
import math
import random
import time

class Player(pygame.sprite.Sprite):
    """The player class"""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("textures/player.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.og_img = self.image
        self.og_img.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(width=32, height=32)
        self.xspeed = 0
        self.yspeed = 0
        self.health = 10
        self.powerups = [False, False, False]
        self.powerupcheck = [False, False, False]

    def move(self, event):
        global running, level
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
        for wall in pygame.sprite.spritecollide(self, wallgroup, False): #good god this took so long
            if wall.rotation == 0:
                self.inx = False
                self.iny = False
                if self.rect.bottom in range(wall.rect.top, wall.rect.centery) or self.rect.top in range(wall.rect.centery, wall.rect.bottom):
                    self.iny = True
                elif self.rect.right in range(wall.rect.left, wall.rect.centerx) or self.rect.left in range(wall.rect.centerx, wall.rect.right):
                    self.inx = True
                if self.inx and not self.iny:
                    if self.rect.right in range(wall.rect.left, wall.rect.centerx):
                        self.rect.right = wall.rect.left
                        self.xspeed = 0
                    elif self.rect.left in range(wall.rect.centerx, wall.rect.right):
                        self.rect.left = wall.rect.right
                        self.xspeed = 0
                    continue
                elif self.iny and not self.inx:
                    if self.rect.top in range(wall.rect.centery, wall.rect.bottom):
                        self.rect.top = wall.rect.bottom
                        self.yspeed = 0
                    elif self.rect.bottom in range(wall.rect.top, wall.rect.centery):
                        self.rect.bottom = wall.rect.top
                        self.yspeed = 0
                    continue
            else:
                self.inx = False
                self.iny = False
                if self.rect.right in range(wall.rect.left, wall.rect.centerx) or self.rect.left in range(wall.rect.centerx, wall.rect.right):
                    self.inx = True
                elif self.rect.bottom in range(wall.rect.top, wall.rect.centery) or self.rect.top in range(wall.rect.centery, wall.rect.bottom):
                    self.iny = True
                if self.iny and not self.inx:
                    if self.rect.top in range(wall.rect.centery, wall.rect.bottom):
                        self.rect.top = wall.rect.bottom
                        self.yspeed = 0
                    elif self.rect.bottom in range(wall.rect.top, wall.rect.centery):
                        self.rect.bottom = wall.rect.top
                        self.yspeed = 0
                    continue
                elif self.inx and not self.iny:
                    if self.rect.right in range(wall.rect.left, wall.rect.centerx):
                        self.rect.right = wall.rect.left
                        self.xspeed = 0
                    elif self.rect.left in range(wall.rect.centerx, wall.rect.right):
                        self.rect.left = wall.rect.right
                        self.xspeed = 0
                    continue
        if self.powerups[1]:
            if self.powerupcheck[1]:
                self.sbase = pygame.time.get_ticks()
                self.powerupcheck[1] = False
            else:
                if pygame.time.get_ticks() == self.sbase+5000:
                    self.powerups[1] = False
        if self.powerups[2]:
            if self.powerupcheck[2]:
                self.gbase = pygame.time.get_ticks()
                self.powerupcheck[2] = False
            else:
                if pygame.time.get_ticks() == self.gbase+5000:
                    self.powerups[2] = False
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
        self.healthtext = "{(" + ("♥"*self.health) + ")" + ("(O)"*self.powerups[1]) + ("(|_|)"*self.powerups[2]) + "}"
        self.healthbar = mainfont.render(self.healthtext, True, (255, 0, 0))
        self.healthrect = self.healthbar.get_rect(center=(self.rect.centerx, self.rect.centery-20))
        display.blit(self.healthbar, self.healthrect)
        if self.health <= 0:
            playergroup.remove(self)
            titlebar = mainfont.render(f"GAME OVER", True, (255, 0, 0))
            titlerect = titlebar.get_rect(center=(int(SWIDTH/2), int(SHEIGHT/2)))
            display.blit(titlebar, titlerect)
            bulletgroup.empty()
            enemygroup.empty()
            wallgroup.empty()
            powergroup.empty()
            pygame.display.flip()
            playerdeath.play()
            time.sleep(4)
            playergroup.add(self)
            level = 0
            init_level()

class Bullet(pygame.sprite.Sprite):
    """The bullet class"""
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
        self.xc = math.cos(self.angle)*32
        self.yc = math.sin(self.angle)*32
        self.good = good
        if offset:
            self.rect.move_ip(-self.yc*4, -self.xc*4)
    
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
                enemy.timer = 0
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
    """The enemy class"""
    def __init__(self, pos, speed):
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
        self.shootspeed = speed*20
        self.timer = random.randint(0, self.shootspeed)
        self.health = 10
    
    def update(self):
        self.targetx, self.targety = player.rect.center
        self.angle = math.atan2((self.rect.centerx)-self.targetx, (self.rect.centery)-self.targety)
        self.image = pygame.transform.rotate(self.og_img, self.angle*57.2957795131)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.timer += 1
        if self.timer == self.shootspeed:
            self.timer = 0
            bulletgroup.add(Bullet(player.rect.center, self.rect.center, good=False))
            shoot.play()
        self.healthtext = "{(" + ("♥"*self.health) + ")}"
        self.healthbar = mainfont.render(self.healthtext, True, (255, 0, 0))
        self.healthrect = self.healthbar.get_rect(center=(self.rect.centerx, self.rect.centery-20))
        display.blit(self.healthbar, self.healthrect)
        if self.health <= 0:
            enemygroup.remove(self)
            death.play()
            powergroup.add(Powerup(random.randint(0, 2), self.rect.center))


class Wall(pygame.sprite.Sprite):
    """The wall class"""
    def __init__(self, pos, length, rot):
        super().__init__()
        self.image = pygame.image.load("textures/wall0.png")
        self.image.set_colorkey((255, 255, 255))
        self.length = length*64
        self.rotation = rot*90
        self.rect = self.image.get_rect(center=pos)
        self.damage = 0

    def update(self):
        if self.damage > 20:
            wallgroup.remove(self)
            wallbreak.play()
            return
        self.image = pygame.image.load(f"textures/wall{round(self.damage/4)}.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (self.length, 16))
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

class Powerup(pygame.sprite.Sprite):
    """The powerup class"""
    def __init__(self, power, pos):
        super().__init__()
        self.power = power
        self.image = pygame.image.load(f"textures/powerup{self.power}.png")
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(center=pos)
        self.stuck = False
    
    def update(self):
        if pygame.sprite.collide_rect(self, player) and not self.stuck:
            player.powerups[self.power] = True
            player.powerupcheck[self.power] = True
            powergroup.remove(self)


def init_level():
    global level, bulletgroup, enemygroup, wallgroup, powergroup, SHEIGHT, SWIDTH, player, mainfont, display, player
    level += 1
    bulletgroup.empty()
    enemygroup.empty()
    wallgroup.empty()
    powergroup.empty()
    player.rect.centerx = int(SWIDTH/2)
    player.rect.centery = int(SHEIGHT/2)
    player.health = 10
    player.powerups = [False, False, False]
    for wall in range(random.randint(level+2, level+4)):
        w = Wall((random.randint(0, SWIDTH), random.randint(0, SHEIGHT)), random.randint(1, 4), random.randint(0, 1))
        wallgroup.add(w)
    for enemy in range(random.randint(level, level+1)):
        e = Enemy((random.randint(0, SWIDTH), random.randint(0, SHEIGHT)), random.randint(6, math.floor((level)/4)+6))
        enemygroup.add(e)
        while pygame.sprite.spritecollide(e, wallgroup, False):
            e.rect.center = (random.randint(0, SWIDTH), random.randint(0, SHEIGHT))

def init():
    global SHEIGHT, SWIDTH, display, mainfont, titlefont, shoot, death, playerdeath, wallbreak, player, bulletgroup, enemygroup, wallgroup, powergroup, level, running 
    pygame.init()
    #initializing display
    SHEIGHT = 720
    SWIDTH = 1024
    display = pygame.display.set_mode((SWIDTH, SHEIGHT))
    version = 1.0
    pygame.display.set_caption(f"Kaboom {version}")
    mainfont = pygame.font.Font("font/arial.ttf", 24)
    titlefont = pygame.font.Font("font/arial.ttf", 108) 
    #initializing sound
    #sounds from Zapsplat.com
    pygame.mixer.init()
    shoot = pygame.mixer.Sound("sounds/shot.mp3")
    death = pygame.mixer.Sound("sounds/death.mp3")
    playerdeath = pygame.mixer.Sound("sounds/playerdeath.mp3")
    wallbreak = pygame.mixer.Sound("sounds/break.mp3")
    #initializing sprites
    player = Player()
    playergroup = pygame.sprite.GroupSingle()
    bulletgroup = pygame.sprite.Group()
    enemygroup = pygame.sprite.Group()
    wallgroup = pygame.sprite.Group()
    powergroup = pygame.sprite.Group()
    playergroup.add(player)
    level = 0
    init_level()
    running = True
    while running:
        pygame.time.Clock().tick()
        if len(enemygroup) == 0:
            titlebar = mainfont.render(f"Level cleared! Level {level+1} next", True, (0, 255, 0))
            titlerect = titlebar.get_rect(center=(int(SWIDTH/2), int(SHEIGHT/2)))
            display.blit(titlebar, titlerect)
            bulletgroup.empty()
            enemygroup.empty()
            wallgroup.empty()
            powergroup.empty()
            pygame.display.flip()
            init_level()
            time.sleep(2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bulletgroup.add(Bullet(pygame.mouse.get_pos(), player.rect.center))
                    shoot.play()
                    if player.powerups[2]:
                        bulletgroup.add(Bullet(pygame.mouse.get_pos(), player.rect.center, offset=True))
                        shoot.play()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                pass
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

def end():
    pygame.quit()
if __name__ == "__main__":
    init()