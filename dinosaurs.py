import pygame                                           # yay pygame


class dinoKillMain():
    '''The Main dinoKill Class- handles initialization
       and creating game'''
    def __init__(self):
        pygame.init()                                   # starts the... uh... game.
        self.clock = pygame.time.Clock()                # lets us tick forward time without depending on computer lag

        self.controller = Controller()
        self.model = DinoList()
        self.view = DinoView(self)

        self.longneck = pygame.image.load("transparent_longneck.png")   # sets dinosaur image
        ln_w, ln_h = self.longneck.get_size()            # gets size of image so we know where the edges are

        self.food = pygame.image.load("")

    def mainLoop(self):
        '''This is the main loop of the game'''
        self.done = False                                    # initializes for main while loop
        while not self.done:
            self.view.redraw(self)
            self.controller.checkInput(self)                #checks user input
            self.model.update(self)
            self.clock.tick(30)                         # limits FPS by ticking forward a bit at a time
        pygame.quit()


#class Model(object):
    #"""
    #Contains and updates the lists of all the objects bouncing around
    #"""
    #def __init__(self):
    #    self.dinosaurs = []                             # initializes list of dinosaurs

    #def update(self, window):
    #    for dino in self.dinosaurs:           # loops through list of dinosaurs
    #        dino.update(window)

class DinoList(pygame.sprite.Group):
    """
    List of dinosaurs
    inherited methods:
    .add adds a sprite to group
    .remove removes a sprite from group
    .update runs update method of every sprite in group
    .draw blits the image of every sprite in group
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

    def redraw(self, window):
        self.screen.fill(self.green)        # makes green background first
        window.model.draw(window.view.screen)
        for dino in window.model: 
            pygame.draw.rect(self.screen, self.black, [dino.x, dino.y + 40, 40, 5]) # the location is [ x from left , y from top, width, height]
            pygame.draw.rect(self.screen, dino.health, [dino.x, dino.y + 40, dino.hunger*0.4, 5])
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
                if pygame.mouse.get_pressed()[2]:       # right mouse button click
                    Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], window)   # make a dinosaur
                elif pygame.mouse.get_pressed()[1]:     # left mouse button click
                    for dino in window.model:
                        if dino.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                            if dino.hunger > 30:
                                dino.hunger -= 30
                            else:
                                dino.hunger = 1


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
        pygame.sprite.Sprite.__init__(self, window.model) #puts dino in list of dinos
        self.x = x
        self.y = y
        self.living = True
        self.hunger = 1
        self.health = window.view.dkgrn
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 1
        self.image = window.image
        self.rect = self.image.get_rect()

    def rush(self):
        """
        updates dinosaur speed based on hunger level
        """
        self.speed = self.hunger/30.0 + 0.5

    def walk(self, window):
        """
        updates position of dinosaur based on speed
        makes dinosaur bounce off walls
        """
        if self.x > window.view.width-40:             # bounce off right edge
            self.xspeed = -1*self.speed
        elif self.x < 1:                    # bounce off left edge
            self.xspeed = 1*self.speed
        else:
            self.xspeed = cmp(self.xspeed, 0)*self.speed  # update speed
        if self.y < 1:                      # bounce off top edge
            self.yspeed = 1 * self.speed
        elif self.y > window.view.height - 40:         # bounce off bottom edge
            self.yspeed = -1 * self.speed
        else:
            self.yspeed = cmp(self.yspeed, 0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed
        self.rect.x = self.x
        self.rect.y = self.y

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
        self.rush()                                 # determines speed
        self.walk(window)                                 # updates its position
        self.starve(window)
        self.reaper(window)

class Human(pygame.sprite.Sprite):
    """This is where we make humans
    inherited methods:
    .update (see below)
    .kill (removes from all groups)
    .alive  (checks to see if belonging to any groups)"""

    def __init__(self, x, y, window):
        pygame.sprite.Sprite.__init__(self, window.model) #puts dino in list of dinos
        self.x = x
        self.y = y
        self.xspeed = 0
        self.yspeed = 0
        self.speed = 0
        self.image = window.longneck
        self.rect = self.image.get_rect()
        
if __name__ == "__main__":
    MainWindow = dinoKillMain()
    MainWindow.mainLoop()
