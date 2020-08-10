import pygame
import time

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pokemon Game')

black = (0,0,0)
white = (255,255,255)

pkm_width = 136
pkm_height = 151

clock = pygame.time.Clock()
pkm_img = pygame.image.load('blastoise.png')

def pkm(x,y):
    gameDisplay.blit(pkm_img, (x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (int((display_width/2)), int((display_height/2)))
    gameDisplay.fill(white)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.7)
    x_change = 0
    y_change = 0

    gameExit = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

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

        if x <= 0:
            x = 0
        if x >= (display_width - pkm_width):
            x = (display_width - pkm_width)

        if y <= 0:
            y = 0
        if y >= (display_height - pkm_height):
            y = (display_height - pkm_height)

        gameDisplay.fill(white)
        pkm(int(x),int(y))

        pygame.display.update()
        clock.tick(60)

message_display("Round 1")
message_display("Fight!")
game_loop()
pygame.quit()
quit()
