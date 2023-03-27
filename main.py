# This is the module import for making 2d games with Python
import pygame

# This is a module for importing the operating system to help get the path to files
import os

# This initilizes a pygame font library
pygame.font.init()

# Var to set a display height and width
WIDTH, HEIGHT = 900, 500
# Var to display window using a tuple
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Game!")

COLOR = (0, 66, 175,)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0,)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Defining a font I want to use.
HEALTH_FONT =  pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# FPS - Frames Per Second
FPS = 60

# Var that sets how far a object should move when a key is pressed down.
VELOCITY = 5
BULLET_VELOCITY = 10
MAX_BULLETS = 3

# Vars to set spaceship image sizes
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Vars for importing the images for the game. Uses the os module to find the path to the files. 
# These image assets are considered "blits" by pygame.
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

# Var to scale and rotate the yellow spaceship image
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", 'spaceship_red.png'))
# Var to scale and rotate the red spaceship image
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Var for the space background
SPACE =  pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Defining a function to update the display
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # The pygame.blit() method applies blits (image or text assets) to the screen and uses a second argument to define where it's placed initially.
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, ((yellow.x, yellow.y)))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

# Defining a function for handling yellow player movement during the game
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0: # Left
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < BORDER.x: # Right
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0: # Up
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 17: # Down
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x + BORDER.width: # Left
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY + red.width < WIDTH: # Right
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0: # Up
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 17: # Down
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

# Defining a function called "main" to handle the game logic
def main():
    # .Rect() method is used to keep track of something in the window. It takes in 4 arguements: x, y, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = [] 

    red_health = 10
    yellow_health = 10

    # The "clock" var is a method from pygame that allows control of the while loop below
    clock = pygame.time.Clock()
    run = True
    while run:
        # For while loop for getting events in the game
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RETURN and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
            
            if event.type == RED_HIT:
                red_health -= 1
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1

        
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins"

        if yellow_health <= 0:
            winner_text = "Red Wins"

        if winner_text != "":
            draw_winner(winner_text) # Someone won the game.
            break

        # This var is a method from pygame that lets us know what keys are being pressed down.
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
