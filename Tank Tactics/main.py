import sys
import math
import pygame
import pyperclip

from player import Player, Turret
from bullet import Player_bullet
from level import Level
from enemy import Classic_enemy

running = True
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("main.mp3")
pygame.mixer.music.play(-1)

events = []

screen = pygame.display.set_mode([1920, 1080])

screen_center_x = screen.get_width() // 2
screen_center_y = screen.get_height() // 2

menu = "home"
level = 0

logo = pygame.image.load("logo.png")

home_button_selected = "play"
play_button = pygame.image.load("play_button.png")
code_button = pygame.image.load("code_button.png")
home_selected = pygame.image.load("home_selected.png")

choose_level_button_selected = 1
choose_level_selected = pygame.image.load("choose_level_selected.png")
choose_level = pygame.image.load("choose_level.png")

player = Player(1.5, 0.6)
turret = Turret()
level_obj = Level()

def get_button_position(button_image, x_offset=0, y_offset=0):
    return {
        "x": screen_center_x - button_image.get_width() // 2 + x_offset,
        "y": screen_center_y - button_image.get_height() // 2 - y_offset,
    }

def get_mouse_position(x_offset=0, y_offset=0):
    return {
        "x" : x_offset - 960,
        "y" : y_offset + 540,
    }

def render_image(image, x=0, y=0):
    image_position = get_button_position(image, x_offset=x, y_offset=y)
    screen.blit(
        image,
        (image_position["x"], image_position["y"])
    )

def tick():
    global menu, home_button_selected, choose_level_button_selected, running

    screen.fill((0, 0, 0))
    
    if menu == "home":
        # select button
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_DOWN:
                    if home_button_selected == "play":
                        home_button_selected = "code"
                elif event.key == pygame.K_UP:
                    if home_button_selected == "code":
                        home_button_selected = "play"
                # activate button
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if home_button_selected == "play":
                        menu = "choose_level"
                    elif home_button_selected == "code":
                        pyperclip.copy("https://github.com/Zocker-Welt/Tank-Tactics")
        

        # render
        render_image(logo, y=300)
        render_image(home_selected, y=-100 if home_button_selected == "play" else -200)
        render_image(play_button, y=-100)
        render_image(code_button, y=-200)
    elif menu == "choose_level":
        # select button
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = "home"
                if event.key == pygame.K_DOWN:
                    choose_level_button_selected += 1
                elif event.key == pygame.K_UP:
                    choose_level_button_selected -= 1
                # activate button
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    level = choose_level_button_selected
                    menu = "game"
                    # setup objects
                    level_obj.setup(level)
                    player.setup(level, level_obj.hitboxes)
                    turret.setup(level, level_obj.hitboxes)
        
        # bounds
        if choose_level_button_selected < 1:
            choose_level_button_selected = 1
        if choose_level_button_selected > 6:
            choose_level_button_selected = 6
        
        # render
        render_image(choose_level, y=300)
        # main
        level_button = pygame.image.load(f"level{choose_level_button_selected}_button.png")
        render_image(level_button, y=-100)
        
        # up
        if choose_level_button_selected > 1:
            level_button = pygame.image.load(f"level{choose_level_button_selected - 1}_button.png")
            level_button = pygame.transform.scale(level_button, (level_button.get_width() * 0.8, level_button.get_height() * 0.8))
            render_image(level_button, y=0)
        # down
        if choose_level_button_selected < 6:
            level_button = pygame.image.load(f"level{choose_level_button_selected + 1}_button.png")
            level_button = pygame.transform.scale(level_button, (level_button.get_width() * 0.8, level_button.get_height() * 0.8))
            render_image(level_button, y=-200)
    elif menu == "game":
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = "choose_level"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
        player.tick()
        turret.tick()
        turret.x = player.x
        turret.y = player.y
        turret.tick_bullets()
        turret.tick_enemies()

        # render
        
        #for hb in level_obj.hitboxes: pygame.draw.rect(screen, (255, 0, 0), hb)
        #pygame.draw.rect(screen, (0, 0, 255), player.player_rect)
        
        player_texture = pygame.image.load(f"{player.texture}.png")
        player_texture = pygame.transform.rotate(player_texture, player.angle)
        render_image(player_texture, x=player.x, y=player.y)

        turret_texture = pygame.image.load("player_turret.png")
        turret_texture = pygame.transform.rotate(turret_texture, turret.angle)
        render_image(turret_texture, x=turret.x, y=turret.y)

        for bullet in turret.bullets:
            bullet_texture = pygame.image.load("classic_bullet.png")
            bullet_texture = pygame.transform.rotate(bullet_texture, bullet.angle)
            bullet_texture = pygame.transform.scale(bullet_texture, (bullet_texture.get_width() * 0.8, bullet_texture.get_height() * 0.8))
            render_image(bullet_texture, x=bullet.x, y=bullet.y)
        
        for enemy in turret.enemies:
            enemy_texture = pygame.image.load("player_body1.png")
            enemy_texture = pygame.transform.rotate(enemy_texture, enemy.angle)
            render_image(enemy_texture, x=enemy.x, y=enemy.y)

            enemy_turret_texture = pygame.image.load("player_turret.png")
            angle = math.degrees(math.atan2(player.y - enemy.y, player.x - enemy.x))
            enemy_turret_texture = pygame.transform.rotate(enemy_turret_texture, angle)
            render_image(enemy_turret_texture, x=enemy.x, y=enemy.y)

        level_texture = pygame.image.load(f"{level_obj.texture}.png")
        level_texture = pygame.transform.scale(level_texture, (level_texture.get_width() * 2.95, level_texture.get_height() * 2.95))
        render_image(level_texture, x=0, y=0)
            

clock = pygame.time.Clock()
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    tick()
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()