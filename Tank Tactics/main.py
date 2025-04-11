import sys
import pygame
import pyperclip
from player import Player

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

player = Player(2, 0.6)

def get_button_position(button_image, x_offset=0, y_offset=0):
    return {
        "x": screen_center_x - button_image.get_width() // 2 + x_offset,
        "y": screen_center_y - button_image.get_height() // 2 - y_offset,
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
                        pyperclip.copy("text")
        

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
                    player.setup()
        
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
        player.tick()
        #print(player.x, player.y)

        # render
        render_image(logo, x=player.x, y=player.y)

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