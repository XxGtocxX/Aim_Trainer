import math 
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600 # no of pixels for screen

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # initialise a pygame window and display it
pygame.display.set_caption("Aim Trainer") # name of window (optional)

TARGET_INCREMENT = 400 # will appear after 400ms
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30 # sets how many pixels we want it to be off the screen

BG_COLOR = (0, 25, 40) # or we can use string ex: "blue"
LIVES = 3
TOP_BAR_HEIGHT = 50
class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    COLOR2 = "white"

    def __init__(self, x, y): # constructor for target where x and y is pos where the target will be on
        self.x = x # randomly generating the pos
        self.y = y
        self.size = 0  # will be 0 at first and then start growing so grow is set true
        self.grow = True

    def update(self): # updates the siz based on current conditon
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: #target will stop growning as soon as it hits max size
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        # we pass the window whr we wanna draw the circle, colour, center and radius of cirlce
        # we are drwing 4 circles with which overlap each other and give us the ring pattern
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size) # from biggest to smaller circles
        pygame.draw.circle(win, self.COLOR2, (self.x, self.y), self.size * 0.8) 
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6) 
        pygame.draw.circle(win, self.COLOR2, (self.x, self.y), self.size * 0.4) 

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2) # self.x is coordinate of circle and x is of mouse
        return dis <= self.size

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    pygame.display.update() #once we drawn all targets and filled the screen then we call update and call them on screen

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0 # no of targets that we were not able to click
    start_time = time.time() # this tracks how much time has passed and the current time

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60) # regualtes the speed at wich this while loop run
        # if we dont have this then it will vary from processor to processor based on computer
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING) # this is for no causign target to go off the screen
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target) # afer every x seconds it will create a target
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                missses =+ 1

            if click and target.collide(*mouse_pos): # *breaks the tuple into its individual positions
                targets.remove(target)
                target_pressed += 1
        if misses >= LIVES:
            pass # end game

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
    pygame.quit()

if __name__ == "__main__": # this ensures that when we run the file it executes the main function
    main()