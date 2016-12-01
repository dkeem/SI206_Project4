import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

everything = pygame.sprite.Group()


class Knife(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(Knife, self).__init__()
        self.image = pygame.image.load("knife.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(3, 8)

        self.add(groups)

    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            self.velocity = random.randint(3, 8)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y

    def kill(self):
        x, y = self.rect.center
        super(EnemySprite, self).kill()


class Potato(pygame.sprite.Sprite):
    def __init__(self, groups):
        super(Potato, self).__init__()
        self.image = pygame.image.load("potato.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0

        self.groups = [groups]

        self.mega = 1

        self.autopilot = False
        self.in_position = False
        self.velocity = 2

    def update(self):
        x, y = self.rect.center

        if not self.autopilot:
            # Handle movement
            self.rect.center = x + self.dx, y + self.dy

        else:
            if not self.in_position:
                if x != X_MAX/2:
                    x += (abs(X_MAX/2 - x)/(X_MAX/2 - x)) * 2
                if y != Y_MAX - 100:
                    y += (abs(Y_MAX - 100 - y)/(Y_MAX - 100 - y)) * 2

                if x == X_MAX/2 and y == Y_MAX - 100:
                    self.in_position = True
            else:
                y -= self.velocity
                self.velocity *= 1.5
                if y <= 0:
                    y = -30
            self.rect.center = x, y

    def move(self, direction, operation):
        v = 10
        if operation == START:
            if direction in (UP, DOWN):
                self.dy = {UP: -v,
                           DOWN: v}[direction]

            if direction in (LEFT, RIGHT):
                self.dx = {LEFT: -v,
                           RIGHT: v}[direction]

        if operation == STOP:
            if direction in (UP, DOWN):
                self.dy = 0
            if direction in (LEFT, RIGHT):
                self.dx = 0


def main():
    game_over = False
    
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)
    enemies = pygame.sprite.Group()
    empty = pygame.Surface((X_MAX, Y_MAX))
    
    clock = pygame.time.Clock()
    seconds = 0 
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    pygame.font.init()
    font = pygame.font.Font(None, 40)

    potato = Potato(everything)
    potato.add(everything)


    for i in range(10):
        pos = random.randint(0, X_MAX)
        Knife(pos, [everything, enemies])
    while not game_over:
        clock.tick()
        # Check for input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game_over = True
            if not game_over:
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        potato.move(DOWN, START)
                    if event.key == K_LEFT:
                        potato.move(LEFT, START)
                    if event.key == K_RIGHT:
                        potato.move(RIGHT, START)
                    if event.key == K_UP:
                        potato.move(UP, START)
                    if event.key == K_RETURN:
                        if potato.mega:
                            potato.mega -= 1
                            for i in enemies:
                                i.kill()

                if event.type == KEYUP:
                    if event.key == K_DOWN:
                        potato.move(DOWN, STOP)
                    if event.key == K_LEFT:
                        potato.move(LEFT, STOP)
                    if event.key == K_RIGHT:
                        potato.move(RIGHT, STOP)
                    if event.key == K_UP:
                        potato.move(UP, STOP)

        if len(enemies) < 20 and not game_over:
            pos = random.randint(0, X_MAX)
            Knife(pos, [everything, enemies])

        screen.fill((0,0,0))
        time = font.render("Time: " + str(pygame.time.get_ticks()), 1, (255,255,255))
        pygame.display.get_surface().blit(time, (400, 10))

        everything.clear(screen, empty)
        everything.update()
        everything.draw(screen)
        pygame.display.flip()

        
        

    pygame.quit()
    quit()




main()
		
