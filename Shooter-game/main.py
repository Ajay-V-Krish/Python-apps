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
BULLET_VELOCITY = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Shooter-game','Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP =pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Shooter-game','Assets', 'spaceship_red.png'))
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

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if yellow.colliderect(bullet):
            yellow_bullets.remove(bullet)



def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - 2,10,5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height/2 - 2,10,5)
                    red_bullets.append(bullet)
        
        keys_pressed = pygame.key.get_pressed()
        
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
            
        draw(red, yellow)
            
    pygame.quit()
    
if __name__ == '__main__':#It prevents the file from running when it is imported.
    main()
            