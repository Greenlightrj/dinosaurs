import pygame                                           # yay pygame

pygame.init()                                           # starts the... uh... game.

# ------- initial conditions -------

clock = pygame.time.Clock()                             # lets us tick forward time without depending on computer lag

screenx = 500                                           # sets width of screen (as a variable so we can use it later)
screeny = 500                                           # sets height
SCREEN = pygame.display.set_mode((screenx, screeny))    # makes screen thing so we can make it green later
                                                        
WHITE = (255, 255, 255)                                 # Define colors so we can use them later
BLACK = (0, 0, 0)
GREEN = (0, 170, 0)

image = pygame.image.load("transparent_longneck.png")   # sets dinosaur image
img_w, img_h = image.get_size()                         # gets size of image so we know where the edges are

dinosaurs = []                                          # initializes list of dinosaurs


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
        if self.x > screenx-40:             # bounce off right edge
            self.xspeed = -1*self.speed
        elif self.x < 1:                    # bounce off left edge
            self.xspeed = 1*self.speed
        else:
            self.xspeed = cmp(self.xspeed, 0)*self.speed  # update speed
        if self.y < 1:                      # bounce off top edge
            self.yspeed = 1 * self.speed
        elif self.y > screeny - 40:         # bounce off bottom edge
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
            dinosaurs.remove(self)


done = False                                # initializes for main while loop
while not done:
    """
    main program loop
    """
    # takes user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:               # If user clicked close
            done = True                             # gets out of the loop
        elif event.type == pygame.KEYDOWN:          # If user pressed a key
            if event.key == pygame.K_ESCAPE:        # escape key is an escape
                done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:  # when mouse button is clicked
            if pygame.mouse.get_pressed()[2]:       # right mouse button click
                dinosaur = Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])   # make a dinosaur
                dinosaurs.append(dinosaur)          # this line amuses me for no reason

    SCREEN.fill(GREEN)                              # makes green background first

    for dino in dinosaurs:                          # loops through list of dinosaurs
        dino.rush()                                 # determines speed
        dino.walk()                                 # updates its position
        dino.starve()
        dino.reaper()
        SCREEN.blit(image, (dino.x, dino.y))        # draws the dino

    pygame.display.flip()                           # actually draws all that stuff.
    clock.tick(30)                                  # limits FPS by ticking forward a bit at a time

pygame.quit                                         # if you exit the loop (done = true) then game closes
