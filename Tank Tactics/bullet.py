from pygame import Rect

import math

screen_offset_x = 960
screen_offset_y = -540

class Player_bullet:
    def __init__(self, x, y, angle, hitboxes):
        self.x = x
        self.y = y
        self.angle = angle
        self.hitboxes = hitboxes
    
    def bound_collision(self):
        if abs(self.x) > 630 or abs(self.y) > 435:
            return True
        return False
    
    def level_collision(self):
        self.player_rect = Rect(self.x + screen_offset_x - 10, -10 - self.y - screen_offset_y, 20, 20)
        for hitbox in self.hitboxes:
            if self.player_rect.colliderect(hitbox):
                return True
        return False

    def tick(self):
        self.x += math.cos(math.radians(self.angle)) * 5
        self.y += math.sin(math.radians(self.angle)) * 5
        self.dead = self.bound_collision() or self.level_collision()
