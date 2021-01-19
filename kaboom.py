import pygame
import math

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("textures/player.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect(width=32, height=32)
        self.rect.x = int(SWIDTH/2)
        self.rect.y = int(SHEIGHT/2)
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
        print(self.xspeed, self.yspeed)

#initializing display
SHEIGHT = 720
SWIDTH = 1024
pygame.init()
display = pygame.display.set_mode((SWIDTH, SHEIGHT))
version = "Alpha 0.0.1"
pygame.display.set_caption(f"Kaboom {version}")
#initializing sprites
player = Player()
playergroup = pygame.sprite.GroupSingle()
playergroup.add(player)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display.fill((0, 127, 255))
    playergroup.draw(display)
    player.move(pygame.key.get_pressed())
    pygame.display.flip()
pygame.quit()