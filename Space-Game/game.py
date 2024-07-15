import pygame
import time
import random
pygame.font.init() #Initializing font in pygame

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')

BG = pygame.transform.scale(pygame.image.load('Space-game/bg.png'), (WIDTH, HEIGHT))#Adding background to the window.

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 80

PLAYER_VELOCITY = 5 #It describes how much pixels player has to move when key is pressed.

FONT = pygame.font.SysFont('Arial', 30) #Setting default font.

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 4

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f'Time: {round(elapsed_time)}s', 1, 'white') #It displays the time.
    WIN.blit(time_text, (10,10))
    
    pygame.draw.rect(WIN, "red", player)#player is the pygame rectangle we have to draw.
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    
    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)#first two are coordinates and the next two are width and height.
    clock = pygame.time.Clock()#It slows the movement of the player.
    
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    hit = False
    
    while run:
        star_count += clock.tick(60)#It returns the number of milli seconds since the last tick. 
        elapsed_time = time.time() - start_time
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH-STAR_WIDTH)
                star = pygame.Rect(star_x,-STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT ) #Negative height is given so that the star appears,to fall from above the screen.
                stars.append(star)
                
            star_add_increment = max(200, star_add_increment-50)#It goes on increasing the stars with time.
            star_count = 0
        
        for event in pygame.event.get(): #Getting event from list of events in pygame.
            if event.type == pygame.QUIT: #Gettin the event of remove in the upper right corner.
                run = False
                break
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0: #It stops the player to move out of the left screen.
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH: #It stops the player to move out of the right screen.
            player.x += PLAYER_VELOCITY
            
        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
            
        if hit:
            lost_text = FONT.render('You Lost',5,'white')
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(3000)
            break
            
        draw(player, elapsed_time, stars)
    
    pygame.quit()
    
if __name__ == '__main__':
    main()