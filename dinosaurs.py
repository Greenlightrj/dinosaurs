import pygame   # yay pygame

pygame.init()  # starts the... uh... game.

#------- initial conditions -------

# lets us tick forward time without depending on computer lag
clock = pygame.time.Clock()

screenx = 500   # sets width of screen (as a variable so we can use it later)
screeny = 500   # sets width
# makes screen thing so we can make it green later
SCREEN = pygame.display.set_mode((screenx, screeny))

# Define colors so we can use them later
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 170, 0)

image = pygame.image.load("plain_longneck.png")     # sets dinosaur image
# gets size of image so we know where the edges are
img_w, img_h = image.get_size()

dinosaurs = []  # initializes list of dinosaurs


class Dino():
    def __init__(self, x, y):   # dinos start alive with 0 hunger
        self.alive = True
        self.hunger = 0
        self.x = x
        self.y = y
        self.xspeed = 1
        self.yspeed = 1

    def speed(self):    # in the future this will make hungry dinos faster
        self.xspeed = 1
        self.yspeed = 1

    def walk(self):
        if self.x >= screenx-50 or self.x < 10:
            self.xspeed = self.xspeed*-1
        if self.y > screeny-50 or self.y < 10:
            self.yspeed = -1 * self.yspeed
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed

done = False

while not done:  # loop all the functions run inside

    # takes user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # If user clicked close
            done = True                 # gets out of the loop
        elif event.type == pygame.KEYDOWN:  # If user pressed a key
            if event.key == pygame.K_ESCAPE:   # escape key is an escape
                done = True
        # when mouse button is clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:    # right mouse button click
                dinosaur = Dino(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])   # make a dinosaur
                dinosaurs.append(dinosaur)  # this line amuses me for no reason

    SCREEN.fill(GREEN)  # makes green background first

    # inner workings update
    for dino in dinosaurs:     # loops through list of dinosaurs
        dino.walk()     # updates its position
        SCREEN.blit(image, (dino.x, dino.y))    # draws the dino

    pygame.display.flip()  # actually draws all that stuff.
    clock.tick(60)  # limits FPS by ticking forward a bit at a time

pygame.quit  # if you exit the loop (done = true) then game closes
