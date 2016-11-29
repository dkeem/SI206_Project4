from pygame import *
from pygame.sprite import *
from random import *

X_MAX = 800
Y_MAX = 600

LEFT, RIGHT, UP, DOWN = 0, 1, 3, 4
START, STOP = 0, 1

bgcolor = (0,0,0)  

class Knife(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = image.load("knife.bmp").convert_alpha()
        self.rect = self.image.get_rect()

    # move gold to a new random location
    def update(self):
        x, y = self.rect.center

        if y > Y_MAX:
            x, y = random.randint(0, X_MAX), 0
            self.velocity = random.randint(3, 10)
        else:
            x, y = x, y + self.velocity

        self.rect.center = x, y



class Potato(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("potato.bmp").convert_alpha()
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.center = mouse.get_pos()



def main():
	init()
	screen = display.set_mode((X_MAX, Y_MAX))

	potato = Potato()
	knife = Knife()
	sprites = RenderPlain(knife, potato)

	while True:
	    e = event.poll()
	    if e.type == QUIT:
	        quit()
	        break

	    screen.fill(bgcolor)

	    # update and redraw sprites
	    sprites.update()
	    sprites.draw(screen)
	    display.update()

main()
