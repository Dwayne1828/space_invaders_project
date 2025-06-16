import pygame 
from pygame.locals import *

# Set Frames per second
clock = pygame.time.Clock()
fps = 60

#Initialize the interface
screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")


#Define colors
red = (225, 0, 0)
green = (0, 225, 0 )


#Load background image
bg = pygame.image.load("img/bg.png")

def draw_bg(): 
    screen.blit(bg, (0, 0))


#Create the spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = health
        self.health_remaining = health

    def update(self):
        #Set Movement Speed
        speed = 8 
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0: 
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width: 
            self.rect.x += speed

        #health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.y + 70), self.rect.width, 10))
        if self.health_remaining > 0: 
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.y + 70), 
                                             int(self.rect.width * (self.health_remaining / self.health_start)), 10))



#Create sprite groups
spaceship_group = pygame.sprite.Group()


#Create the spaceship object
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)


#Loop for the game to run
run = True 
while run:

    clock.tick(fps)

    draw_bg()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    #update spaceship
    spaceship.update()

    #update sprite groups
    spaceship_group.draw(screen)

    pygame.display.update()

pygame.quit()
    

