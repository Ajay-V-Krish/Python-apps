import pygame
import time
import math
import os
pygame.font.init()

def scale_images(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    
def blit_text_centre(win, font,text):
    render = font.render(text, 1, (205,205,205))
    win.blit(render, (win.get_width()/2-render.get_width()/2,win.get_height()/2 - render.get_height()/2))

GRASS_BG = scale_images(pygame.image.load(os.path.join('Car-Game','imgs','grass.jpg')), 2.5)
TRACK = scale_images(pygame.image.load(os.path.join('Car-Game','imgs','track.png')), 0.9)

TRACK_BORDER = scale_images(pygame.image.load(os.path.join('Car-Game','imgs','track-border.png')),0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load(os.path.join('Car-Game','imgs','finish.png'))
FINISH_POSITION = (130,250)
FINISH_MASK = pygame.mask.from_surface(FINISH)

RED_CAR = scale_images(pygame.image.load(os.path.join('Car-Game','imgs','red-car.png')),0.55)
GREEN_CAR =scale_images(pygame.image.load(os.path.join('Car-Game','imgs','green-car.png')), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont('comicsans', 44)

FPS = 60
PATH = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]

class GameInfo:
    LEVELS = 10
    
    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.start_time = 0
        
    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = 1
        self.started = False
        self.start_time = 0
        
    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.start_time = time.time()
        
    def level_time(self):
        if not self.started:
            return 0
        return self.start_time - time.time()

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        
    def rotate(self, left = False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
            
    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
        
    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        
        self.y -= vertical
        self.x -= horizontal
    
    def collide(self, mask, x=0,y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi
    
    def reset(self):
        self.x,self.y = self.START_POS
        self.angle = 0
        self.vel = 0

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180,200)
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()
        
    def bounce(self):
        self.vel = -self.vel
        self.move()
        
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150,200)
    
    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
        
    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255,0,0), point, 5)
            
    def draw(self, win):
        super().draw(win)
        # self.draw_points(win)
        
    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        
        if y_diff == 0:
            desired_radian_angle = math.pi/2
        else:
            desired_radian_angle = math.atan(x_diff/y_diff)
        
        if target_y > self.y:
            desired_radian_angle += math.pi
            
        diff_in_angle = self.angle - math.degrees(desired_radian_angle)
        if diff_in_angle >= 180:
            diff_in_angle -= 360
        
        if diff_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(diff_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(diff_in_angle))
            
    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1
        
    def move(self):
        if self.current_point >= len(self.path):
            return
        self.calculate_angle()
        self.update_path_point()
        super().move()

def draw(win, images, player_car, computer_car, game_info):
    for img,pos in images:
       win.blit(img, pos)
    
    level_text = MAIN_FONT.render(f'Level {game_info.level}', 1, (255,255,255))
    win.blit(level_text,(10, HEIGHT - level_text.get_height()-70))  
    
    time_text = MAIN_FONT.render(f'Time: {game_info.level_time}s', 1, (255,255,255))
    win.blit(time_text,(10, HEIGHT - time_text.get_height()-40))
    
    vel_text = MAIN_FONT.render(f'Vel: {player_car.vel}px/s', 1, (255,255,255))
    win.blit(vel_text,(10, HEIGHT - vel_text.get_height()-10))     
    
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()
    
def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()
        
    if not moved:
        player_car.reduce_speed()
        
def handle_collision(player_car,computer_car):
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()
      
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        player_car.reset()
        computer_car.reset()
          
    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()
            print('finish')

run = True
clock = pygame.time.Clock()
images = [(GRASS_BG, (0,0)), (TRACK, (0,0)), (FINISH,FINISH_POSITION), (TRACK_BORDER,(0,0))]
player_car = PlayerCar(4,4)
computer_car = ComputerCar(4,4,PATH)
game_info = GameInfo()

while run:
    clock.tick(FPS)
    draw(WIN, images, player_car, computer_car, game_info)
    
    while not game_info.started:
        blit_text_centre(WIN, MAIN_FONT, f'Press any key to start level {game_info.level}!')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            if event.type == pygame.KEYDOWN:
                game_info.start_level()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
            break
        
        
    move_player(player_car)
    computer_car.move()   
     
    handle_collision(player_car, computer_car)
    
    
# print(computer_car.path)
pygame.quit()