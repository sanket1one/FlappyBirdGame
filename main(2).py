import pygame, sys, random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos  = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (576, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (576, random_pipe_pos - 150))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


pygame.init()  # initialising the pygame
screen = pygame.display.set_mode((576, 1024))  # (width,height) of the canvas display
clock = pygame.time.Clock()  # used for controlling the frame rate

# game variable
gravity = 0.25
bird_movement = 0
game_active = True

bg_surface = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_surface = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [350, 250, 200]

while True:  # game loop(all logic of game)
    for event in pygame.event.get():  # event loop (whichever events that will take place,are in here)
        if event.type == pygame.QUIT:  # adds the quit button on display
            pygame.quit()  # exits the game
            sys.exit()  # completely shuts down the game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12

            if event.key == pygame.k_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface, (0, 0))
    # 'blit' overlaps one surface over another surface using the coordinates


if game_active:
    # Bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)
    game_active = check_collision(pipe_list)

    # Pipes
    pipe_list = move_pipe(pipe_list)
    draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()  # whatever we add in loop gets updated on display
    clock.tick(120)  # frames per second