import pygame                                           # yay pygame
from math import sin, cos, atan2, hypot
import random

class dinoKillMain():
    '''The Main dinoKill Class- handles initialization
       and creating game'''
    def __init__(self):
        pygame.init()                                   # starts the... uh... game.
        self.clock = pygame.time.Clock()                # lets us tick forward time without depending on computer lag
        self.controller = Controller()
        self.model = Model()
        self.view = DinoView(self)

        self.longneck = pygame.image.load("transparent_longneck.png")   # sets dinosaur image

        self.food = pygame.image.load("man.png")

    def mainLoop(self):
        '''This is the main loop of the game'''
        self.done = False                                    # initializes for main while loop
        while not self.done:
            self.view.redraw(self)
            self.controller.checkInput(self)                #checks user input
            self.model.update(self)
            self.clock.tick(30)                         # limits FPS by ticking forward a bit at a time
        pygame.quit()


class Model(object):
    """holds the lists and updates"""
    def __init__(self):
        self.predators = DinoList()
        self.food = HumanList()

    def update(self, window):
        self.predators.update(window)
        self.food.update(window)

        for dino in self.predators:
            noms = pygame.sprite.spritecollide(dino, self.food, 0, collided = None)
            for man in noms:
                if dino.hunger > 30:
                    dino.hunger -= 30
                else:
                    dino.hunger = 1
                man.kill()


class DinoList(pygame.sprite.Group):
    """
    List of dinosaurs
    inherited methods:
    .add adds a sprite to group
    .remove removes a sprite from group
    .update runs update method of every sprite in group
    .draw blits the image of every sprite in group
    """


class HumanList(pygame.sprite.Group):
    """
    list of humans
    """


class DinoView():
    """
    Deals with drawing of the background
    """
    def __init__(self, window, width=500, height=500):
        self.width = width                              # sets width of screen (as a variable so we can use it later)
        self.height = height                            # sets height
        self.screen = pygame.display.set_mode((self.width, self.height))    # makes screen thing so we can make it green later
        self.green = (0, 170, 0)
        self.dkgrn = (16, 65, 0)                       #define colors
        self.black = (0, 0, 0)
        self.red = (200, 0, 0)
        self.orange = (250, 65, 0)
        self.dkgrey = (20, 20, 20)
        self.font = pygame.font.SysFont(None,20)

    def redraw(self, window):
        self.screen.fill(self.green)        # makes green background first
        self.text = self.font.render('Dinosaurs alive: ' + str(len(MainWindow.model.predators)),True, self.dkgrn)
        window.model.predators.draw(window.view.screen)
        for dino in window.model.predators:
            pygame.draw.rect(self.screen, self.black, [dino.rect.x, dino.rect.y + 40, 40, 5]) # the location is [ x from left , y from top, width, height]
            pygame.draw.rect(self.screen, dino.health, [dino.rect.x, dino.rect.y + 40, dino.hunger*0.4, 5])
        window.model.food.draw(window.view.screen)
        self.screen.blit(self.text,(10,10))
        pygame.display.flip()                       # actually draws all that stuff.
        

class Controller():
    """Does things based on user input"""
    def __init__(self):
        pass

    def checkInput(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # If user clicked close
                window.done = True
            elif event.type == pygame.KEYDOWN:          # If user pressed a key
                if event.key == pygame.K_ESCAPE:        # escape key is an escape   
                    window.done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # when mouse button is clicked
                if pygame.mouse.get_pressed()[0]:     # left mouse button click
                    Human(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], window)   # make a human
                elif pygame.mouse.get_pressed()[2]:       # right mouse button click
                    Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], window)   # make a dinosaur
                
class Dino(pygame.sprite.Sprite):
    """
    This is where we make dinosaurs
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)
    """
    def __init__(self, x, y, window):
        """
        dinos start alive with 1 hunger
        """
        pygame.sprite.Sprite.__init__(self, window.model.predators) #puts dino in list of dinos
        self.image = window.longneck
        self.rect = self.image.get_rect()
        self.x = x  #actual position, can be float
        self.y = y
        self.rect.x = x     #integer position for drawing
        self.rect.y = y
        self.living = True
        self.hunger = 1
        self.health = window.view.dkgrn
        self.angle = random.randrange(-314, 314)
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 1

    def rush(self):
        """
        updates dinosaur speed based on hunger level
        """
        self.speed = self.hunger/30.0 + 0.5

    def hunt(self, window):
        """
        lets dino track toward humans within range
        range is based on hunger
        """
        for man in window.model.food:
            if hypot(self.x - man.x, self.y - man.y) < self.hunger*5:
                self.angle = 100*atan2(man.y - self.y, man.x - self.x)

    def walk(self, window):
        """
        updates position of dinosaur based on speed
        makes dinosaur bounce off walls
        """
        if self.x > window.view.width - 40:             # bounce off right edge
            self.angle = random.randrange(157,471)
        elif self.x < 1:                    # bounce off left edge
            self.angle = random.randrange(-157,157)
        if self.y < 1:                      # bounce off top edge
            self.angle = random.randrange(0, 314)
        elif self.y > window.view.height - 40:         # bounce off bottom edge
            self.angle = random.randrange(-314,0)
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def starve(self, window):
        """
        updates dinosaur hunger
        """
        if self.hunger < 30:
            self.health = window.view.dkgrn
            self.hunger += 0.03
        elif self.hunger < 75:
            self.health = window.view.orange
            self.hunger += 0.03
        elif self.hunger < 100:
            self.health = window.view.red
            self.hunger += 0.03
        else:
            self.living = False

    def reaper(self, window):
        """
        gets rid of dead dinosaurs
        """
        if self.living is False:
            self.kill()

    def update(self, window):
        self.rush()                            # determines speed
        self.hunt(window)
        self.walk(window)                      # updates its position
        self.starve(window)
        self.reaper(window)


class Human(pygame.sprite.Sprite):
    """This is where we make humans
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)"""

    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model.food)  #puts human in list of humans
        self.image = window.food
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.angle = random.randint(-314, 314)
        self.speed = 1
        self.xspeed = 1
        self.yspeed = 1

    def flee(self, window):
        """
        humans run from nearest dinosaur
        there's a problem with this somewhere.. it doesn't work if there aren't dinos
        """
        if len(window.model.predators.sprites()) > 0:     #if there are any dinos
            dist = 1000000
            for dino in window.model.predators:
                if hypot(dino.x - self.x, dino.y - self.y) < dist:
                    dist = hypot(dino.x - self.x, dino.y - self.y)
                    nearest = dino
            self.angle = 100*atan2(self.y - nearest.y, self.x - nearest.x)


    def run(self, window):
        """
        humans walk around randomly if there are no dinos
        humans can escape via the edges
        """
        if self.x > window.view.width:
            self.kill()
        elif self.x < 1:
            self.kill()
        if self.y < 1:
            self.kill()
        elif self.y > window.view.height:
            self.kill()
        self.yspeed = sin(self.angle/100.0)*self.speed  # update speed
        self.xspeed = cos(self.angle/100.0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def splat(self, window):
        """
        leaves bloodstain and skull for a while
        """
        pass

    def update(self, window):
        self.flee(window)
        self.run(window)

if __name__ == "__main__":
    MainWindow = dinoKillMain()
    MainWindow.mainLoop()
