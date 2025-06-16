import pygame 
from pygame import mixer
from pygame.locals import *
import random

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Set Frames per second
clock = pygame.time.Clock()
fps = 60

#Initialize the interface
screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")


font30 = pygame.font.SysFont("Constantia", 30)
font40 = pygame.font.SysFont("Constantia", 40)


#Load Sounds
explosion_fx = pygame.mixer.Sound("img/explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("img/explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25)


#Define global variables
rows = 5
cols = 5
alien_cooldown = 500  # milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3 
last_count = pygame.time.get_ticks()
game_over = 0  #0 no game over, 1 is winner, -1 means lost


#Define colors
red = (225, 0, 0)
green = (0, 225, 0 )
white = (255, 255, 255)


#Load background image
bg = pygame.image.load("img/bg.png")

def draw_bg(): 
    screen.blit(bg, (0, 0))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Create the spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #Set Movement Speed
        speed = 8 
        cooldown = 500  # milliseconds
        game_over = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and self.rect.left > 0: 
            self.rect.x -= speed
        if key[pygame.K_d] and self.rect.right < screen_width: 
            self.rect.x += speed

        #Check the last shot time
        time_now = pygame.time.get_ticks()

        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            #Create a bullet and add it to the bullet group
            laser_fx.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        #health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.y + 70), self.rect.width, 10))
        if self.health_remaining > 0: 
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.y + 70), 
                                             int(self.rect.width * (self.health_remaining / self.health_start)), 10))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over 


#Create the bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0: 
            self.kill()
        if pygame.sprite.spritecollide(self, aliens_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)


#Create the aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.move_direction = 1
        self.move_counter = 0 
        self.move_speed = 2
    
    def update(self):
        self.rect.x += self.move_direction * self.move_speed
        self.move_counter += self.move_speed
        if abs(self.move_counter) > 60: 
            self.move_direction *= -1 
            self.move_counter *= -1


#Create the bullet class
class AlienBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        self.rect.y += 3
        if self.rect.bottom > screen_height: 
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            spaceship.health_remaining -= 1
            self.kill()
            explosion2_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)


#Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = [] 
        for num in range(1,6):
            explosion_image = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                explosion_image = pygame.transform.scale(explosion_image, (20, 20))
            if size == 2:
                explosion_image = pygame.transform.scale(explosion_image, (40, 40))
            if size == 3: 
                explosion_image = pygame.transform.scale(explosion_image, (160, 160))
            self.images.append(explosion_image)
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0 

    def update(self):
        explosion_speed = 3 
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0 
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()



#Create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
aliens_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()


def create_aliens():
    for row in range(rows):
        for col in range(cols): 
            alien = Aliens(100 + col * 100, 100 + row * 70)
            aliens_group.add(alien)

create_aliens()


#Create the spaceship object
spaceship = Spaceship(int(screen_width / 2), screen_height - 100, 3)
spaceship_group.add(spaceship)

#Loop for the game to run
run = True 
while run:

    clock.tick(fps)

    draw_bg()

    if countdown == 0: 
        #Random alien bullet
        time_now = pygame.time.get_ticks()
        #shoot
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 10 and len(aliens_group) > 0:
            attacking_alien = random.choice(aliens_group.sprites())
            alien_bullet = AlienBullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False


        #If winner
        if len(aliens_group) == 0:
            game_over = 1

        if game_over == 0: 
            #update spaceship
            game_over = spaceship.update()

            #update sprite groups
            bullet_group.update()
            aliens_group.update()
            alien_bullet_group.update()
        else:
            if game_over == -1:
                draw_text("Game Over!", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1: 
                draw_text("You Win!", font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))


    if countdown > 0:
        draw_text("Get Ready!", font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = countdown


    #Update Explosion Group
    explosion_group.update()

    #update sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    aliens_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    pygame.display.update()

pygame.quit()
    

