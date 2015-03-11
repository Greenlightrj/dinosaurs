import pygame                                           # yay pygame


class dinoKillMain(object):
    '''The Main dinoKill Class- handles initialization
       and creating game'''
    def __init__(self):
        pygame.init()                                   # starts the... uh... game.
        self.clock = pygame.time.Clock()                # lets us tick forward time without depending on computer lag

        self.controller = Controller()
        self.model = Model()
        self.view = DinoView()

        self.image = pygame.image.load("transparent_longneck.png")   # sets dinosaur image
        img_w, img_h = self.image.get_size()            # gets size of image so we know where the edges are

    def mainLoop(self, window):
        '''This is the main loop of the game'''
        self.done = False                                    # initializes for main while loop
        while not self.done:
            self.controller.checkInput(self)                #checks user input
            self.view.redraw(self)
            self.model.update(window)

            self.clock.tick(30)                         # limits FPS by ticking forward a bit at a time
        pygame.quit()


class Model(object):
    """
    Contains and updates the lists of all the objects bouncing around
    """
    def __init__(self):
        self.dinosaurs = []                             # initializes list of dinosaurs

    def update(self, window):
        for dino in self.dinosaurs:           # loops through list of dinosaurs
            dino.update(window)


class DinoView(object):
    """
    Deals with drawing of the background
    """
    def __init__(self, width=500, height=500):
        self.width = width                              # sets width of screen (as a variable so we can use it later)
        self.height = height                            # sets height
        self.screen = pygame.display.set_mode((self.width, self.height))    # makes screen thing so we can make it green later

        self.green = (0, 170, 0)
        self.dkgrn = (16, 65, 0)                       #define colors
        self.black = (0, 0, 0)
        self.red = (200, 0, 0)
        self.orange = (250, 65, 0)

    def redraw(self, window):
        self.screen.fill(self.green)        # makes green background first
        for dino in window.model.dinosaurs: # draws the dinosaurs
            window.view.screen.blit(window.image, (dino.x, dino.y))
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
                    dinosaur = Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], window)   # make a dinosaur
                    window.model.dinosaurs.append(dinosaur)    # add dino to list of all dinos
                

class Dino():
    """
    This is where we make dinosaurs
    """

    def __init__(self, x, y, window):
        """
        dinos start alive with 1 hunger
        """
        self.alive = True
        self.hunger = 1
        self.health = window.view.dkgrn
        self.x = x
        self.y = y
        self.xspeed = 1
        self.yspeed = 1
        self.speed = 1

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
            self.alive = False

    def reaper(self, window):
        """
        gets rid of dead dinosaurs
        """
        if self.alive == False:
            window.model.dinosaurs.remove(self)

    def update(self, window):
        self.rush()                                 # determines speed
        self.walk(window)                                 # updates its position
        self.starve(window)
        self.reaper(window)

if __name__ == "__main__":
    MainWindow = dinoKillMain()
    MainWindow.mainLoop(MainWindow)
