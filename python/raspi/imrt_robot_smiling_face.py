import pygame
import random

def drawEye(pos, ball_size, pup_size, view_dir):
    ball_corner = (pos[0] - ball_size[0] / 2, pos[1] - ball_size[1] / 2)
    pup_pos = (int(pos[0] + view_dir[0] * (ball_size[0] / 2 - pup_size)),
               int(pos[1] + view_dir[1] * (ball_size[1] / 2 - pup_size)))
    pygame.draw.ellipse(surface, WHITE, ball_corner + ball_size, 0)
    pygame.draw.ellipse(surface, BLACK, ball_corner + ball_size, 2)
    pygame.draw.circle(surface, BLACK, pup_pos, 20, 0)

win_x = 800
win_y = 480
win_size = [win_x,win_y]

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = (  0, 154, 129)
eye_spacing = 200

l_eye_pos_x = 0
l_eye_pos_y = 0
r_eye_pos_x = 0
r_eye_pos_y = 0

pygame.init()

win = pygame.display

win.set_caption('Robot eyes')

surface = win.set_mode(win_size)

mouth = pygame.image.load('mouth_382_crop.png')
welcome = pygame.image.load('welcome.png')

clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

window = True
w_c = 0
while window:

    surface.fill(GREEN)
    drawEye(( (win_x + eye_spacing) / 2, win_y * 7 / 18), (160, 200), 20, (l_eye_pos_x, l_eye_pos_y))
    drawEye(( (win_x - eye_spacing) / 2, win_y * 7 / 18), (160, 200), 20, (r_eye_pos_x, r_eye_pos_y))

    if (random.randint(0, 200) == 100):
        l_eye_pos_x = (-0.5 + random.random()) * 1.6
        l_eye_pos_y = (-0.5 + random.random()) * 1.6

    if (random.randint(0, 200) == 100):
        r_eye_pos_x = (-0.5 + random.random()) * 1.6
        r_eye_pos_y = (-0.5 + random.random()) * 1.6

    mouth_x = (win_x - mouth.get_rect().width) / 2 + random.randint(-4, 4)
    mouth_y = win_y * 11 / 18 + random.randint(-4, 4)
    surface.blit(mouth, (mouth_x, mouth_y))
    
    if w_c < 48:
        surface.blit(welcome, (0, 480-w_c*10))
    elif w_c < 200:
        surface.blit(welcome, (0, 0))
    elif w_c < 248:
        surface.blit(welcome, (0, (w_c-200)*10))


    pygame.display.update()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            window = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                window = False

        
    w_c = (w_c + 1) % 1000
    clock.tick(40)

    
