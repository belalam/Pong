import pygame
from pygame.locals import *


class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize
        self.centerx = int(screensize[0] * 0.5)
        self.centery = int(screensize[1] * 0.5)
        self.radius = 10
        self.rect = pygame.Rect(self.centerx - self.radius,
                                self.centery - self.radius,
                                self.radius * 2, self.radius * 2)
        self.colour = (255, 255, 255)
        self.direction = [-1, 1]
        self.speedx = 2
        self.speedy = 5

        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle=None, ai_paddle=None):

        self.centerx += self.direction[0] * self.speedx
        self.centery += self.direction[1] * self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1] - 1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0] - 1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

    def render(self, screen):
        pygame.draw.circle(screen, self.colour, self.rect.center, self.radius, 0)


class AIPaddle(object):
    def __init__(self, screensize):

        self.screen_size = screensize
        self.centerx = 5
        self.centery = int(screensize[1] * 0.5)

        self.height = 100
        self.width = 10
        self.color = (255, 100, 100)

        self.rect = pygame.Rect(0, self.centery - int(self.height * 0.5), self.width, self.height)

        self.speed = 5

    def update(self, pong):

        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)


class PlayerPaddle(object):
    def __init__(self, screensize):

        self.screensize = screensize
        self.centerx = screensize[0] - 5
        self.centery = int(screensize[1] * 0.5)

        self.height = 100
        self.width = 10
        self.color = (100, 255, 100)

        self.rect = pygame.Rect(0, self.centery - int(self.height * 0.5), self.width, self.height)

        self.speed = 4
        self.direction = 0

    def update(self):
        self.centery += self.direction * self.speed

        if self.centery < int(self.height * 0.5):
            self.centery = int(self.height * 0.5)
        if self.centery > (self.screensize[1] - 1) - int(self.height * 0.5):
            self.centery = (self.screensize[1] - 1) - int(self.height * 0.5)

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)


def main():
    pygame.init()

    screensize = (640, 480)

    screen = pygame.display.set_mode(screensize)

    clock = pygame.time.Clock()

    pong = Pong(screensize)
    player_paddle = PlayerPaddle(screensize)
    ai_paddle = AIPaddle(screensize)

    running = True

    while running:

        # limit fps
        clock.tick(64)

        # event handling phase
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
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

        # object update phase
        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)

        if pong.hit_edge_left:
            print 'You Won!'
            running = False

        elif pong.hit_edge_right:
            print 'You Lose!'
            running = False

        # rendering phase
        screen.fill((0, 0, 0))
        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)
        pygame.display.flip()

    pygame.quit()


main()