import pygame
import os

WIDTH, HEIGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spacecraft Shooter')

BORDER = pygame.Rect((WIDTH/2) - 5, 0, 10, HEIGHT)
BORDER_COLOR = (0,0,0)

BACKGROUND = (255,255,255)

FPS = 60 #It defines the speed of the game in different computers.(Frames per second).
VELOCITY = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP =pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)


def draw(red, yellow):
    WINDOW.fill(BACKGROUND)
    pygame.draw.rect(WINDOW, BORDER_COLOR, BORDER)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x,red.y))
    pygame.display.update()
    
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: #YELLOW LEFT
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x - VELOCITY + yellow.width < BORDER.x: #YELLOW RIGHT 
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: #YELLOW TOP
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 20: #YELLOW BOTTOM
        yellow.y += VELOCITY
        
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: #RED LEFT
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x - VELOCITY + red.width < WIDTH: #RED RIGHT
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: #RED TOP
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 20: #RED BOTTOM
        red.y += VELOCITY


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys_pressed = pygame.key.get_pressed()
        
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)
            
        draw(red, yellow)
            
    pygame.quit()
    
if __name__ == '__main__':#It prevents the file from running when it is imported.
    main()
            