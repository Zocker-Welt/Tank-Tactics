from pygame import key, K_SPACE
from pygame import K_w, K_a, K_s, K_d
from pygame import K_LEFT, K_RIGHT
from pygame import Rect

from time import time
import math

from bullet import Player_bullet
from enemy import Classic_enemy

screen_offset_x = 960
screen_offset_y = -540

class Player:
    def __init__(self, speed, resistance):
        self.speed = speed
        self.resistance = resistance
        self.texture = "player_body1"
    
    def setup(self, level, hitboxes):
        self.x = 0
        self.y = 0
        self.vel_x = 0
        self.vel_y = 0
        self.angle = 0
        self.hitboxes = hitboxes
    
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
        self.level_collision()
        keys = key.get_pressed()
        if keys[K_a]:
            self.vel_x -= self.speed
        if keys[K_d]:
            self.vel_x += self.speed
        if keys[K_w]:
            self.vel_y += self.speed
        if keys[K_s]:
            self.vel_y -= self.speed
        # change pos
        self.vel_x *= self.resistance
        self.vel_y *= self.resistance
        self.x += self.vel_x
        if self.bound_collision() or self.level_collision():
            self.x -= self.vel_x
            self.vel_x = 0
        self.y += self.vel_y
        if self.bound_collision() or self.level_collision():
            self.y -= self.vel_y
            self.vel_y = 0
        # animate
        if abs(self.vel_x) >= 0.1 and abs(self.vel_y) >= 0.1:
            self.texture = f"player_body{round(time() * 100) % 2 + 1}"
        else:
            self.texture = "player_body1"
        # rotate
        if self.vel_x == 0 and self.vel_y == 0:
            self.angle = 0  # or any other default angle
        else:
            self.angle = math.degrees(math.atan2(self.vel_y, self.vel_x))
            if self.angle < 0:
                self.angle += 360

class Turret:
    def setup(self, level, hitboxes):
        self.last_shot = time()
        self.x = 0
        self.y = 0
        self.angle = 0
        self.bullets = []
        self.hitboxes = hitboxes
        self.level = level
        self.generate_enemies()
    
    def generate_enemies(self):
        self.enemies = []
        match self.level:
            case 1:
                self.enemies.extend([
                    Classic_enemy(0, 0, self.hitboxes)
                ])
    
    def tick_bullets(self):
        bullets_copy = self.bullets.copy()
        for bullet in bullets_copy:
            bullet.tick()
            if bullet.dead:
                self.bullets.remove(bullet)
    
    def tick_enemies(self):
        for enemy in self.enemies:
            enemy.tick()
    
    def tick(self):
        keys = key.get_pressed()
        # dir
        if keys[K_LEFT]:
            self.angle += 5
        if keys[K_RIGHT]:
            self.angle -= 5
        if self.angle < 0:
            self.angle += 360
        # shoot
        keys = key.get_pressed()
        if time() - self.last_shot >= 1:
            # can shoot
            if keys[K_SPACE]:
                self.last_shot = time()
                self.bullets.append(Player_bullet(self.x, self.y, self.angle, self.hitboxes))