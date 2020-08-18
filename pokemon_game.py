import pygame
import time
import math
import random

pygame.init()
clock = pygame.time.Clock()

# dimensions of game window
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pokemon Game')

# colors
black = (0,0,0)
white = (255,255,255)
blue = (0, 155, 255)
red = (255, 155, 0)
full_red = (255, 0, 0)
full_blue = (0, 0, 255)

# pokemon images
pkm_img = pygame.image.load('blue_eyes_white_dragon.png')
computer_pkm = pygame.image.load('charizard.png')

# player_wins is a global bool to keep track of who won
player_wins = True

# fireballs array: [ [angle, x_coord, y_coord], [angle, x_coord, y_coord], ... ]
fireballs = []
comp_fireballs = []

# image sizes
pkm_width = pkm_img.get_rect().width
pkm_height = pkm_img.get_rect().height
comp_pkm_width = computer_pkm.get_rect().width
comp_pkm_height = computer_pkm.get_rect().height

# function to display pokemon
def pkm(img, x, y):
    gameDisplay.blit(img, (x,y))

# helper function for message_display
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# function to display text to screen
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int((display_width/2)), int((display_height/2)))
    gameDisplay.fill(white)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(1)

# full health global variable
full_health = 200

# function to display health meter
def display_health(surf, x, y, color, health):
    pygame.draw.rect(surf, color, [x, y, health, 20])
    pygame.draw.lines(surf, black, 0, [(x,y), (x,y+20)], 2)
    pygame.draw.lines(surf, black, 0, [(x,y), (x+full_health,y)], 2)
    pygame.draw.lines(surf, black, 0, [(x,y+20), (x+full_health,y+20)], 2)
    pygame.draw.lines(surf, black, 0, [(x+full_health,y), (x+full_health,y+20)], 2)

# game events set in the game_loop function
def game_loop():

    # declare any global variables needed
    global player_wins
    
    # starting position
    x = (display_width * 0.1)
    y = (display_height * 0.5)
    x_change = 0
    y_change = 0
    angle = 0

    # computer starting position
    comp_x = (display_width * 0.8)
    comp_y = (display_height * 0.5)
    comp_x_change = 0
    comp_y_change = 0
    comp_angle = 3.1415

    # local variables to help with the event loop
    gameExit = False
    tick = 0
    comp_health = full_health
    player_health = full_health
    
    while not gameExit:
        tick += 1
        # mouse position used to rotate pokemon
        initial_mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            # arrow keys for motion
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                elif event.key == pygame.K_DOWN:
                    y_change += 5
                elif event.key == pygame.K_UP:
                    y_change -= 5
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    y_change = 0

            # add fireball to fireball array if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                fireballs.append([angle, x+120, y+50])
                
            # add fireball to comp_fireball array at random time
            if (tick % 10 == 0):
                comp_angle = -math.atan2(comp_y - y, comp_x - x)*57.2958
                comp_fireballs.append([comp_angle, comp_x+20, comp_y+20])

        # player pokemon motion
        x += x_change
        y += y_change

        # prevent pokemon from running off the page
        if x <= 0:
            x = 0
        if x >= ((display_width/2) - pkm_width - 20):
            x = ((display_width/2) - pkm_width - 20)

        if y <= 55:
            y = 55
        if y >= (display_height - pkm_height):
            y = (display_height - pkm_height)

        # rotate pokemon if mouse moves
        mouse_pos = pygame.mouse.get_pos()
        if (mouse_pos != initial_mouse_pos):
            angle = math.atan2(mouse_pos[1] - (y + pkm_height/2), mouse_pos[0] - (x + pkm_width/2)) * 57.2958
            
        pkm_img_rot = pygame.transform.rotate(pkm_img, -angle)

        # computer pokemon motion
        if (tick % 50 == 0):
            comp_x_change = 5 * random.randint(-1, 1)
            comp_y_change = 5 * random.randint(-1, 1)
        comp_x += comp_x_change
        comp_y += comp_y_change

        # prevent computer pokemon from running off the page
        if comp_x <= (display_width / 2) + 20:
           comp_x = (display_width / 2) + 20
        if comp_x >= (display_width - comp_pkm_width):
            comp_x = (display_width - comp_pkm_width)
        if comp_y <= 55:
            comp_y = 55
        if comp_y >= (display_height - comp_pkm_height):
            comp_y = (display_height - comp_pkm_height)

        # shoot all the fireballs in the fireball array, if any
        for fireball in fireballs:
            idx = 0
            velx = math.cos(fireball[0] / 57.2958)*10
            vely = math.sin(fireball[0] / 57.2958)*10
            fireball[1] += velx
            fireball[2] += vely
            # remove fireballs from array when they go off screen
            if fireball[1] <-10 or fireball[1] >810 or fireball[2] <-10 or fireball[2] >610:
                fireballs.pop(idx)
            # remove fireball from array if it hits target
            if (fireball[1] > (comp_x + 5) and fireball[1] < (comp_x + 65)):
                if (fireball[2] > (comp_y + 15) and fireball[2] < (comp_y + 90)):
                    fireballs.pop(idx)
                    # reduce computer health since it got hit
                    comp_health -= 5
                    if (comp_health == 0):
                        player_wins = True
                        gameExit = True
                        
            idx += 1

        # shoot all the fireballs in the comp_fireball array
        for comp_fireball in comp_fireballs:
            comp_idx = 0
            comp_velx = -math.cos(comp_fireball[0] / 57.2958)*10
            comp_vely = math.sin(comp_fireball[0] / 57.2958)*10
            comp_fireball[1] += comp_velx
            comp_fireball[2] += comp_vely
            # remove comp_fireballs from array when they off screen
            if comp_fireball[1] <-10 or comp_fireball[1] >810 or comp_fireball[2] <-10 or comp_fireball[2] >610:
                comp_fireballs.pop(comp_idx)
            # remove fireball from array if it hits target
            if (comp_fireball[1] > (x + 5) and comp_fireball[1] < (x + 95)):
                if (comp_fireball[2] > (y + 15) and comp_fireball[2] < (y + 120)):
                    comp_fireballs.pop(comp_idx)
                    # reduce player health since it got hit
                    player_health -= 5
                    if (player_health == 0):
                        player_wins = False
                        gameExit = True
                        
            comp_idx += 1
        
        # paint background, pokemon, dividing line, and fireballs, and health meters
        gameDisplay.fill(white)
        pkm(pkm_img_rot, int(x),int(y))
        pkm(computer_pkm, int(comp_x), int(comp_y))
        pygame.draw.rect(gameDisplay, black, [int(display_width/2), 0, 10, display_height])
        for projectile in fireballs:
            pygame.draw.circle(gameDisplay, blue, [int(projectile[1]), int(projectile[2])], 10)
        for comp_projectile in comp_fireballs:
            pygame.draw.circle(gameDisplay, red, [int(comp_projectile[1]), int(comp_projectile[2])], 10)

        display_health(gameDisplay, (display_width - (full_health + 20)), 30, full_red, comp_health)
        display_health(gameDisplay, 20, 30, full_blue, player_health)
        
        pygame.display.update()
        clock.tick(60)

# main function
message_display("Round 1")
message_display("Fight!")
game_loop()
if (player_wins == True):
    message_display("You win!")
else:
    message_display("You lose!")
time.sleep(2)
pygame.quit()
quit()
