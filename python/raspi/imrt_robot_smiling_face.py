import pygame
import random
from math import cos, sin, sqrt, pi



def draw_eye(eye_pos, ball_size, pup_size, view_angle, view_offset):
    '''
    This function draws an eye on the screen
    '''

    # pygame uses corner of rectangle as posistion for ellipses, our function uses center
    ball_corner = (eye_pos[0] - ball_size[0] / 2, eye_pos[1] - ball_size[1] / 2)
    
    # draw ellipses
    pygame.draw.ellipse(surface, WHITE, (ball_corner, ball_size), 0)
    pygame.draw.ellipse(surface, BLACK, (ball_corner, ball_size), 2)

    # calculate ellipse radius at given view angle
    ellipse_radius = ball_size[0]/2 * ball_size[1]/2 * sqrt(1 / ((ball_size[1]/2)**2 * cos(view_angle)**2 + (ball_size[0]/2)**2 * sin(view_angle)**2))

    # calculate pupile x and y
    pup_x = int( eye_pos[0] + (view_offset * (ellipse_radius - pup_size)) * cos(view_angle) )
    pup_y = int( eye_pos[1] + (view_offset * (ellipse_radius - pup_size)) * sin(view_angle) )

    # draw pupile
    pygame.draw.circle(surface, BLACK, (pup_x, pup_y), 20, 0)



# windows size
win_x = 800
win_y = 480
win_size = [win_x,win_y]

# pygame setup
pygame.init()
win = pygame.display
win.set_caption('Robot eyes')
surface = win.set_mode(win_size)
clock = pygame.time.Clock()

# load mouth image
mouth = pygame.image.load('mouth_382_crop.png')

# define some colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 154, 129)

# initial view angle and offset values
l_eye_angle = 0
l_eye_offset = 0
r_eye_angle = 0
r_eye_offset = 0

# eye spacing
eye_spacing = 200

# full screen (comment this line to disable full screen at startup)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


window = True

while window:

    # set background color
    surface.fill(GREEN)
    
    # make mouth shake by moving it slightly at random
    mouth_x = int((win_x - mouth.get_rect().width) / 2 + random.randint(-4, 4))
    mouth_y = int(win_y * 11 / 18 + random.randint(-4, 4))
    
    # draw mouth
    surface.blit(mouth, (mouth_x, mouth_y))
    
    # change left eye values at random
    if (random.randint(0, 200) == 100):
        l_eye_angle = random.random() * 2 * pi
        l_eye_offset = random.random()

    # change right eye values at random
    if (random.randint(0, 200) == 100):
        r_eye_angle = random.random() * 2 * pi
        r_eye_offset = random.random()

    # draw eyes
    draw_eye(( (win_x + eye_spacing) / 2, win_y * 7 / 18), (160, 200), 20, l_eye_angle, l_eye_offset)
    draw_eye(( (win_x - eye_spacing) / 2, win_y * 7 / 18), (160, 200), 20, r_eye_angle, r_eye_offset)

    # update display
    pygame.display.update()

    # check and handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            window = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window = False

    # sleep for a while
    clock.tick(40)

    
