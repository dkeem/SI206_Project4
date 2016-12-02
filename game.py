import random
import sys

import pygame
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
    K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

every_sprite = pygame.sprite.Group()


class Knife(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(Knife, self).__init__()
        self.image = pygame.image.load("knife.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        self.velocity = random.randint(1, 5)

        self.add(groups)

    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            # self.velocity = random.randint(1, 5)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y

    def kill(self):
        x, y = self.rect.center
        super(Knife, self).kill()


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

    def hit(self, target):
        return self.rect.colliderect(target)



def main():
    
    pygame.init()
    
    #sets the dimension of the screen
    screen = pygame.display.set_mode((X_MAX, Y_MAX), DOUBLEBUF)

    #Manage how fast screen updates
    clock = pygame.time.Clock()

    #List of knives
    knives = pygame.sprite.Group()

    #Potato or the sprite you control
    potato = Potato(every_sprite)
    every_sprite.add(potato)

    empty = pygame.Surface((X_MAX, Y_MAX))

    #Sets timer of the game
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

    #Creates the font for any text in the game
    font = pygame.font.Font(None, 40)

    #Adds 5 knives to the screen at random -- This is "level one"
    for i in range(5):
        position = random.randint(0, X_MAX)
        Knife(position, [every_sprite, knives])

    game_running = True
    

    game_over = False
    while not game_over:
        # Check for input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                game_over = True
                break
            #If key is press down, start moving
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    potato.move(DOWN, START)
                if event.key == K_LEFT:
                    potato.move(LEFT, START)
                if event.key == K_RIGHT:
                    potato.move(RIGHT, START)
                if event.key == K_UP:
                    potato.move(UP, START)
                # if event.key == K_RETURN:
                #     if potato.mega:
                #         potato.mega -= 1
                #         for i in enemies:
                #             i.kill()

            #Once key is not pressed down, stop the movement
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    potato.move(DOWN, STOP)
                if event.key == K_LEFT:
                    potato.move(LEFT, STOP)
                if event.key == K_RIGHT:
                    potato.move(RIGHT, STOP)
                if event.key == K_UP:
                    potato.move(UP, STOP)

        #Shows the time
        screen.fill(BLACK)
        time = font.render("Time: " + str(pygame.time.get_ticks() / 1000), 1, (255,255,255))
        pygame.display.get_surface().blit(time, (325, 10))

        #"level two"
        if (pygame.time.get_ticks() / 1000) > 5 and (pygame.time.get_ticks() / 1000) <= 10 and len(knives) <= 8:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(3,8)
        #"level three"
        elif (pygame.time.get_ticks() / 1000) > 10  and (pygame.time.get_ticks() / 1000) <= 15 and len(knives) <= 13:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(3,9)

        elif (pygame.time.get_ticks() / 1000) > 15  and (pygame.time.get_ticks() / 1000) <= 20 and len(knives) <= 17:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(5,9)

        elif (pygame.time.get_ticks() / 1000) > 20  and (pygame.time.get_ticks() / 1000) <= 30 and len(knives) <= 17:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(5,10)

        elif (pygame.time.get_ticks() / 1000) > 30  and (pygame.time.get_ticks() / 1000) <= 60 and len(knives) <=20:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(7,10)

        elif (pygame.time.get_ticks() / 1000) > 60  and (pygame.time.get_ticks() / 1000) <= 100 and len(knives) <=27:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(7,10)

        elif (pygame.time.get_ticks() / 1000) > 100 and len(knives) <=34:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).velocity = random.randint(7,15)



        #See if potato collided with the knives
        potato_got_cut = pygame.sprite.spritecollide(potato, knives, True)

        #If potato collided with knives, game is basically over
        
            
            


    

        every_sprite.clear(screen, empty)
        every_sprite.update()
        every_sprite.draw(screen)
        pygame.display.flip()

    if potato_got_cut:
        every_sprite.empty()
        knives.empty()
        main()
    
    pygame.quit()
    quit()


                    
main()
		
