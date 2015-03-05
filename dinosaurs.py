import pygame                                           # yay pygame


class dinoKillMain:
    '''The Main dinoKill Class- handles initialization
       and creating game'''
    def __init__(self, width=500, height=500):
        pygame.init()                                   # starts the... uh... game.
        self.clock = pygame.time.Clock()                # lets us tick forward time without depending on computer lag

        self.controller = Controller()
        self.width = width                              # sets width of screen (as a variable so we can use it later)
        self.height = height                            # sets height
        self.screen = pygame.display.set_mode((self.width, self.height))    # makes screen thing so we can make it green later

        self.green = (0, 170, 0)                        #define colors

        self.image = pygame.image.load("transparent_longneck.png")   # sets dinosaur image
        img_w, img_h = self.image.get_size()            # gets size of image so we know where the edges are

        self.dinosaurs = []                             # initializes list of dinosaurs

    def mainLoop(self):
        '''This is the main loop of the game'''
        done = False                                    # initializes for main while loop
        while not done:
            # takes user input
            self.controller.checkInput()
            view = DinoView()
            view.redraw()
            for dino in MainWindow.dinosaurs:           # loops through list of dinosaurs
                dino.update()
            pygame.display.flip()                       # actually draws all that stuff.
            self.clock.tick(30)                         # limits FPS by ticking forward a bit at a time
        pygame.quit
        sys.exit()


class DinoView():
    def __init__(self,width=500,height=500):
        pass

    def redraw(self):
        MainWindow.screen.fill(MainWindow.green)        # makes green background first


class Controller():
    def __init__(self):
        pass
    def checkInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:               # If user clicked close
                done = True                             # gets out of the loop
                sys.exit()
            elif event.type == pygame.KEYDOWN:          # If user pressed a key
                if event.key == pygame.K_ESCAPE:        # escape key is an escape   
                    done = True
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # when mouse button is clicked
                if pygame.mouse.get_pressed()[2]:       # right mouse button click
                    dinosaur = Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])   # make a dinosaur
                    MainWindow.dinosaurs.append(dinosaur)    # add dino to list of all dinos


class Dino():
    def __init__(self, x, y):
        """
        dinos start alive with 1 hunger
        """
        self.alive = True
        self.hunger = 1
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

    def walk(self):
        """
        updates position of dinosaur based on speed
        makes dinosaur bounce off walls
        """
        if self.x > MainWindow.width-40:             # bounce off right edge
            self.xspeed = -1*self.speed
        elif self.x < 1:                    # bounce off left edge
            self.xspeed = 1*self.speed
        else:
            self.xspeed = cmp(self.xspeed, 0)*self.speed  # update speed
        if self.y < 1:                      # bounce off top edge
            self.yspeed = 1 * self.speed
        elif self.y > MainWindow.height - 40:         # bounce off bottom edge
            self.yspeed = -1 * self.speed
        else:
            self.yspeed = cmp(self.yspeed, 0)*self.speed  # update speed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed

    def starve(self):
        """
        updates dinosaur hunger
        """
        if self.hunger < 100:
            self.hunger += 0.03
        else:
            self.alive = False

    def reaper(self):
        """
        gets rid of dead dinosaurs
        """
        if self.alive == False:
            MainWindow.dinosaurs.remove(self)
    def update(self):
        self.rush()                                 # determines speed
        self.walk()                                 # updates its position
        self.starve()
        self.reaper()
        MainWindow.screen.blit(MainWindow.image, (self.x, self.y))        # draws the dino

if __name__ == "__main__":
    MainWindow = dinoKillMain()
    MainWindow.mainLoop()
