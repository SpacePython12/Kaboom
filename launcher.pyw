from tkinter import *
from PIL import ImageTk, Image
from source import *
import source
import pygame
import math
import random
import time
import threading

def play():
    pygame.mixer.init()
    shoot = pygame.mixer.Sound("sounds/shot.mp3")
    death = pygame.mixer.Sound("sounds/death.mp3")
    playerdeath = pygame.mixer.Sound("sounds/playerdeath.mp3")
    wallbreak = pygame.mixer.Sound("sounds/break.mp3")
    game = threading.Thread(target=source.init)
    game.start()

def creds():
    credwin = Toplevel(screen)
    credwin.title("Credits")
    credtxt = open("accessories/creds.txt").read()
    credlab = Label(credwin, text=credtxt)
    credlab.pack()

screen = Tk()
screen.title("Play Kaboom")
screen.protocol("WM_DELETE_WINDOW", source.end)
title = Label(screen, text="Play Kaboom", font="Arial 24 bold")
title.pack()
scr = ImageTk.PhotoImage(Image.open("textures/screen.png"), size=0.5)
scrlabel = Label(screen, image=scr)
scrlabel.pack()
sourcecode = open("source.pyw").read()
playb = Button(screen, text="Play", font="Arial 16 bold", width=7, height=1, command=lambda: play())
playb.pack()
credb = Button(screen, text="Credits", font="Arial 8", command=lambda: creds())
credb.pack(side=RIGHT)

mainloop()