import pygame as pg
import random
from Settings import *
from Sprites import *

class Game:
    def __init__(self):
        #initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.level = 0
    
    def createplatform(self, x, y, w, h):
        platform = Platform(x, y, w, h)
        self.all_sprites.add(platform)
        self.platforms.add(platform)

    def createlava(self, x, y, w, h):
            lava = Lava(x, y, w, h)
            self.all_sprites.add(lava)
            self.platforms.add(lava)

    def room1(self):
        self.createplatform(0, HEIGHT - 40, WIDTH / 2, 40)
        self.createplatform(300, HEIGHT * 3 / 4, 200, 20)
        self.createlava(WIDTH / 2, HEIGHT -40, WIDTH / 2, 40)

    def room2(self):
            self.createplatform(40, 400, 40, 20)
            self.createplatform(200, 400, 40, 20)
            self.createplatform(440, 400, 40, 20)
            self.createlava(0, HEIGHT -40, WIDTH, 40)

    def removeplatforms(self):
        for platform in self.platforms:
            self.platforms.remove(platform)
            self.all_sprites.remove(platform)

    def nextlevel(self):
        self.removeplatforms()
        if self.level == 0:
            self.room1()
        elif self.level == 1:
            self.room2()
        self.level += 1


         
    def new(self):
        #Start new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.nextlevel()
        self.run()
       
    def run(self):
        # Gameloop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


    def update(self):
        #Game loop - Update
        self.all_sprites.update()
        

    def events(self):
        #Game loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False 

    def draw(self):
        #Game loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # after drawing everything, flip the display
        pg.display.flip()


g = Game()
while g.running:
    g.new()

pg.quit()