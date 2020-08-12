import pygame
import time
import math

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

# pokemon image
pkm_img = pygame.image.load('blastoise.png')

# image sizes
pkm_width = pkm_img.get_rect().width
pkm_height = pkm_img.get_rect().height

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

# game events set in the game_loop function
def game_loop():
    
    # starting position
    x = (display_width * 0.45)
    y = (display_height * 0.7)
    x_change = 0
    y_change = 0

    gameExit = False
    
    while not gameExit:
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
        
        x += x_change
        y += y_change

        # prevent pokemon from running off the page
        if x <= 0:
            x = 0
        if x >= (display_width - pkm_width):
            x = (display_width - pkm_width)

        if y <= 0:
            y = 0
        if y >= (display_height - pkm_height):
            y = (display_height - pkm_height)

        # use mouse to rotate pokemon
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(mouse_pos[1] - (y + pkm_height/2), mouse_pos[0] - (x + pkm_width/2)) * 57.2958
        angle = -1 * (angle + 180)
        pkm_img_rot = pygame.transform.rotate(pkm_img, angle)

        # first paint background, then paint pokemon over background
        gameDisplay.fill(white)
        pkm(pkm_img_rot, int(x),int(y))

        pygame.display.update()
        clock.tick(60)

# main function
message_display("Round 1")
message_display("Fight!")
game_loop()
pygame.quit()
quit()
