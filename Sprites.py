import pygame as pg
from Settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(50, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 1)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        if keys[pg.K_UP]:
            if self.touchingground():
                self.acc.y = JUMP_FORCE

        ground = self.touchingground()
        if ground:
            self.pos.y = ground.rect.top
            self.vel.y = 0
            self.rect.bottom = ground.rect.top
            if isinstance(ground, Lava):
                self.game.playing = False
                self.game.room1()

        roof = self.touchingroof()
        if roof:
            self.vel.y = 0
            self.rect.top = roof.rect.bottom
            #self.pos.y = roof.rect.bottom + self.rect.height
            self.pos = self.rect.midbottom
            
        sides = self.touchingside(ground)
        if sides:
            if (self.rect.left > sides.rect.right):
                self.rect.left = sides.rect.right
            elif (self.rect.right < sides.rect.left):
                self.rect.right = sides.rect.left
            self.vel.x = 0
            self.acc.x = 0
            self.pos = self.rect.midbottom

        #apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        #make the player stop at edge of screen/go to next level
        if self.pos.x > WIDTH:
            self.pos = vec(WIDTH / 2, HEIGHT / 2)
            self.rect.midbottom = self.pos
            self.game.nextlevel()

        if self.pos.x < 0:
            self.vel.x = 0
            self.pos.x = 0

        self.rect.midbottom = self.pos
        

    def touchingground(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for platform in hits:
            if (self.rect.bottom > platform.rect.top and 
               self.rect.bottom < platform.rect.top + 20 and
               self.rect.right > platform.rect.left and
               self.rect.left < platform.rect.right):
                return platform
        return
    
    def touchingroof(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for platform in hits:
            if ((self.rect.top < platform.rect.bottom and 
               self.rect.bottom > platform.rect.bottom) and
               
               self.rect.right > platform.rect.left and
               self.rect.left < platform.rect.right):
                return platform
        return
    
    def touchingside(self, ground):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for platform in hits:
            if (platform != ground and
                self.rect.top < platform.rect.bottom and 
                self.rect.bottom > platform.rect.top + 10 and
                (self.rect.right > platform.rect.left and
                self.rect.left < platform.rect.left) or
                (self.rect.left < platform.rect.right and
                self.rect.right > platform.rect.right)):
                return platform
        return
    

        
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
