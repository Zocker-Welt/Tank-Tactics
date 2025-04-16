from pygame import Rect

from time import time
from random import randint
import math

screen_offset_x = 960
screen_offset_y = -540

class Classic_enemy:
    # uses player texture
    def __init__(self, x, y, hitboxes):
        self.x = x
        self.y = y
        self.hitboxes = hitboxes
        self.angle = 0
        self.angle_change = -1 if randint(0, 1) else 1
        self.turret_angle = 0

    def bound_collision(self):
        if abs(self.x) > 630 or abs(self.y) > 435:
            return True
        return False
    
    def level_collision(self):
        self.player_rect = Rect(self.x + screen_offset_x - 25, -25 - self.y - screen_offset_y, 50, 50)
        for hitbox in self.hitboxes:
            if self.player_rect.colliderect(hitbox):
                return True
        return False

    def tick(self):
        if round(time()) % 3 == 0:
            self.angle += self.angle_change
        else:
            self.angle_change = -1 if randint(0, 1) else 1
            dx = math.cos(math.radians(self.angle)) * 2
            dy = math.sin(math.radians(self.angle)) * 2
            self.x += dx
            if self.bound_collision() or self.level_collision():
                self.x -= dx
            self.y += dy
            if self.bound_collision() or self.level_collision():
                self.y -= dy