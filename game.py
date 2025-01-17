#NAME: David Kim
#UNIQUENAME: dkeem
#Project 4
#GAME TITLE: French-Fried

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

#Knife sprite which you have to dodge
class Knife(pygame.sprite.Sprite):
    def __init__(self, x_pos, groups):
        super(Knife, self).__init__()
        self.image = pygame.image.load("knife.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, 0)

        #initial velocity of knives falling
        self.speed = random.randint(1, 5)

        self.add(groups)


    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
        else:
            x, y = x, y + self.speed

        self.rect.center = x, y


#The potato sprite that you control
class Potato(pygame.sprite.Sprite):
    def __init__(self, groups):
        super(Potato, self).__init__()
        self.image = pygame.image.load("potato.bmp").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (X_MAX/2, Y_MAX - 40)
        self.dx = self.dy = 0

        self.groups = [groups]


    def update(self):
        x, y = self.rect.center

        self.rect.center = x + self.dx, y + self.dy


    #determines how "fast" the sprite moves
    def move(self, direction, operation):
        distance = 10
        if operation == START:
            if direction in (UP, DOWN):
                self.dy = {UP: -distance,
                           DOWN: distance}[direction]

            if direction in (LEFT, RIGHT):
                self.dx = {LEFT: -distance,
                           RIGHT: distance}[direction]

        if operation == STOP:
            if direction in (UP, DOWN):
                self.dy = 0
            if direction in (LEFT, RIGHT):
                self.dx = 0

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
    
    #accumulates point
    point_count = 0

    #Creates the font for any text in the game
    font = pygame.font.Font(None, 40)

    #background music
    pygame.mixer.music.load("song.wav")
    pygame.mixer.music.play(-1, 0.0)

    #Adds 5 knives to the screen at random -- This is "level one"
    for i in range(5):
        position = random.randint(0, X_MAX)
        Knife(position, [every_sprite, knives])

    

    game_over = False
    while not game_over:
        # Check for input
        # clock.tick(60)
        point_count += 1
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

        #Shows the points you accumulated and divided by 25 to make points smaller
        screen.fill(BLACK)
        points = font.render("POINTS: " + str(point_count//25), 1, (255,255,255))
        pygame.display.get_surface().blit(points, (325, 10))

        #"level two" based on how many points you've accumulated
        if (point_count//25) > 5 and (point_count//25) <= 10 and len(knives) <= 8:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(3,8)
        #"level three"
        elif (point_count//25) > 10  and (point_count//25) <= 15 and len(knives) <= 13:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(3,9)

        #"level four"
        elif (point_count//25) > 15  and (point_count//25) <= 20 and len(knives) <= 17:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(5,9)

        #"level five"
        elif (point_count//25) > 20  and (point_count//25) <= 30 and len(knives) <= 17:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(5,10)

        #"level six"
        elif (point_count//25) > 30  and (point_count//25) <= 60 and len(knives) <=20:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(7,10)

        #"level seven"
        elif (point_count//25) > 60  and (point_count//25) <= 100 and len(knives) <=27:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(7,10)

        #"level eight"
        elif (point_count//25) > 100 and len(knives) <=34:
            position = random.randint(0, X_MAX)
            Knife(position, [every_sprite, knives])
            Knife(position, [every_sprite, knives]).speed = random.randint(7,15)



        #See if potato collided with the knives
        potato_got_cut = pygame.sprite.spritecollide(potato, knives, True)

        #If potato collided with knives, game is basically over
        if potato_got_cut:
            pygame.mixer.music.stop()
            pygame.mixer.Sound("SLICED.wav").play()
            every_sprite.empty()
            knives.empty()
            pygame.mixer.music.load("song2.wav")
            pygame.mixer.music.play(-1, 0.0)
            for i in range(50):
                fried_message = font.render("YOU GOT FRENCH-FRIED", 1, (WHITE))
                pygame.display.get_surface().blit(fried_message, (245, 275))
                end_points = font.render("YOU GOT " + str(point_count//25) + " POINTS", 1, (WHITE))
                pygame.display.get_surface().blit(end_points, (250, 325))
                pygame.display.flip()

            main()
            
    

        every_sprite.clear(screen, empty)
        every_sprite.update()
        every_sprite.draw(screen)
        pygame.display.flip()

    
    pygame.quit()
    quit()


if __name__ == "__main__":
    while True:
        main()
		
