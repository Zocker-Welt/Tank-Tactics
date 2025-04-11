from pygame import key
from pygame import K_SPACE
from pygame import K_w
from pygame import K_a
from pygame import K_s
from pygame import K_d
from pygame import K_UP
from pygame import K_DOWN
from pygame import K_LEFT
from pygame import K_RIGHT

class Player:
    def __init__(self, speed, resistance):
        self.speed = speed
        self.resistance = resistance
    
    def setup(self):
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
    
    def tick(self):
        keys = key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.vel_x -= self.speed
        if keys[K_d] or keys[K_RIGHT]:
            self.vel_x += self.speed
        if keys[K_w] or keys[K_UP]:
            self.vel_y += self.speed
        if keys[K_s] or keys[K_DOWN]:
            self.vel_y -= self.speed
        self.vel_x *= self.resistance
        self.vel_y *= self.resistance
        self.x += self.vel_x
        self.y += self.vel_y