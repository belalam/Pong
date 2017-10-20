import pygame
from pygame.locals import *
import Objects

running=True
pygame.init()

def main(running):

    screensize = (640,480)

    screen = pygame.display.set_mode(screensize)

    clock = pygame.time.Clock()

    #initialize objects
    start_button = Objects.Button(screensize, "START", 1)
    again_button = Objects.Button(screensize, "Go Again?", 1)
    exit_button = Objects.Button(screensize, "QUIT", 2)
    pong = Objects.Pong(screensize)
    player_paddle = Objects.PlayerPaddle(screensize)
    ai_paddle = Objects.AIPaddle(screensize)


    #set states
    menu=True
    play=False

    while menu:
        clock.tick(64)
        start_button.render(screen)
        exit_button.render(screen)
        pygame.display.flip()
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # event handling phase
        if start_button.rect.collidepoint(mouse) and mouse_click[0] == True:
            menu = False
            play = True

        if exit_button.rect.collidepoint(mouse) and mouse_click[0] == True:
            menu = False
            running = False

        for event in pygame.event.get():
            if event.type == QUIT:
                menu=False
                running = False

    while play:

        clock.tick(64)
        # event handling phase
        for event in pygame.event.get():
            if event.type == QUIT:
                play = False
                running = False
                pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player_paddle.direction = -1
            elif event.key == K_DOWN:
                player_paddle.direction = 1
        if event.type == KEYUP:
            if event.key == K_UP and player_paddle.direction == -1:
                player_paddle.direction = 0
            elif event.key == K_DOWN and player_paddle.direction == 1:
                player_paddle.direction = 0


        #object update phase
        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)



        if pong.hit_edge_left:

            myfont = pygame.font.Font('freesansbold.ttf', 30)
            textsurface = myfont.render('You Won!', True, [255, 255, 255])
            text_pin = (int(screensize[0] / 2) - int(myfont.size('You Win!')[0] / 2), 150)
            screen.blit(textsurface, text_pin)
            pygame.display.flip()
            pygame.time.delay(4000)
            play = False






        elif pong.hit_edge_right:

            myfont = pygame.font.Font('freesansbold.ttf', 30)
            textsurface = myfont.render('You Lose!', True, [255, 255, 255])
            text_pin = (int(screensize[0]/2) - int(myfont.size('You Lose!')[0] / 2), 150)
            screen.blit(textsurface, text_pin)
            pygame.display.flip()
            pygame.time.delay(4000)
            play = False


        #rendering phase
        screen.fill((0, 0, 0))
        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)
        pygame.display.flip()

    return running

while running:
    running=main(running)
    if running == False:
        pygame.quit()
