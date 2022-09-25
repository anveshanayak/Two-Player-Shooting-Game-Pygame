import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900, 600
S_WIDTH, S_HEIGHT = 90, 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTING GAME")

FPS = 60
VEL = 5
BUL_VEL = 7
MAX_BULLETS = 3
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
# fonts

LIVES_FONT = pygame.font.SysFont("Lato", 30)
WINNER_FONT = pygame.font.SysFont("Lato", 70)

# events
# creating events for green hit and orange hit

GREEN_HIT = pygame.USEREVENT + 1
ORANGE_HIT = pygame.USEREVENT + 2

# colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


GREEN = (0, 255, 0)
ORANGE = (255, 50, 0)
PURPLE = (15, 10, 30)

# images, elements
# transform is used to modify the dimensions of the images to required size
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Images','space_bg.png')), (WIDTH, HEIGHT))
GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Images','spaceship_green.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (S_WIDTH,S_HEIGHT)), 270)
ORANGE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Images','spaceship_orange.png'))
ORANGE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(ORANGE_SPACESHIP_IMAGE, (S_WIDTH,S_HEIGHT)), 90)
# manage bullets controls the number of bullets remaining, velocity of bullet


def manage_bullets(green_bullets, orange_bullets, green, orange):
    for bullet in green_bullets:
        bullet.x += BUL_VEL
        if orange.colliderect(bullet): #if the bullet from green hits orange hitbox |colliderect is an inbuilt function under pygame.Rect
            pygame.event.post(pygame.event.Event(ORANGE_HIT))
            green_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            green_bullets.remove(bullet)

    for bullet in orange_bullets:
        bullet.x -= BUL_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            orange_bullets.remove(bullet)
        elif bullet.x < 0:
            orange_bullets.remove(bullet)


def green_movement(keys_pressed, green):
    if keys_pressed[pygame.K_a] and green.x - VEL > 0: # left
        green.x -= VEL
    if keys_pressed[pygame.K_d] and green.x + VEL + green.width < BORDER.x: #right
        green.x += VEL
    if keys_pressed[pygame.K_w] and green.y - VEL > 0: # up
        green.y -= VEL
    if keys_pressed[pygame.K_s] and green.y + VEL + green.height < HEIGHT - 20: #down
        green.y += VEL


def orange_movement(keys_pressed, orange):
    if keys_pressed[pygame.K_LEFT] and orange.x - VEL > BORDER.x + BORDER.width: #left
        orange.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and orange.x + VEL + orange.width < WIDTH: #right
        orange.x += VEL
    if keys_pressed[pygame.K_UP] and orange.y - VEL > 0: # up
        orange.y -= VEL
    if keys_pressed[pygame.K_DOWN] and orange.y + VEL + orange.height < HEIGHT -20: # down
        orange.y += VEL


def draw_window(green, orange, green_bullets, orange_bullets, green_lives, orange_lives):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, PURPLE, BORDER)
    orange_lives_text = LIVES_FONT.render("LIVES: " + str(orange_lives), 1, WHITE)
    green_lives_text = LIVES_FONT.render("LIVES: " + str(green_lives), 1, WHITE)
    WIN.blit(orange_lives_text, (WIDTH - green_lives_text.get_width() - 10, 10))
    WIN.blit(green_lives_text, (10, 10))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))
    WIN.blit(ORANGE_SPACESHIP, (orange.x, orange.y))

    for bullet in green_bullets: #drawing/making the bullets show up on the screen
        pygame.draw.rect(WIN, GREEN, bullet)
    for bullet in orange_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)
    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 -
    draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    green = pygame.Rect(100, 300, S_WIDTH, S_HEIGHT) #hitbox
    orange = pygame.Rect(800, 300, S_WIDTH, S_HEIGHT)
    green_bullets = []


    orange_bullets = []
    green_lives = 10
    orange_lives = 10
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                #Start Key Controls
                #Bullet shooting controls for green
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x + green.width, green.y + green.height // 2 + 12, 10, 5)
                    green_bullets.append(bullet)
                #Bullet shooting controls for orange
                if event.key == pygame.K_RCTRL and len(orange_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(orange.x, orange.y + orange.height // 2 + 12, 10, 5)
                    orange_bullets.append(bullet)
            if event.type == GREEN_HIT: #Orange bullet has hit green ship
                green_lives -= 1

            if event.type == ORANGE_HIT: #Green bullet has hit orange ship
                orange_lives -= 1
        winner = ""
        if green_lives <= 0:
            winner = "Orange Wins!!"
        if orange_lives <= 0:
            winner = "Green Wins!!"

        if winner != "":
            draw_winner(winner)
            break

        keys_pressed = pygame.key.get_pressed()
        green_movement(keys_pressed, green)
        orange_movement(keys_pressed, orange)
        manage_bullets(green_bullets, orange_bullets, green, orange)
        draw_window(green, orange, green_bullets, orange_bullets, green_lives, orange_lives)
    main()

if __name__ == "__main__":
    main()