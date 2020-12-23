import random
import pygame
import math

pygame.init()

"""overall control variable"""
ScreenX = 600
ScreenY = 780
PXchange = 1
PYchange = 0
EXchange = 1
EYchange = 32
BX = 0
BY = 700
BXchange = 0
BYchange = 5

#color
RED = (255,0,0)
WHITE = (255,255,255)

screen = pygame.display.set_mode((ScreenX, ScreenY))


# background img
backImg = pygame.image.load('background.png')

def background():
    screen.blit(backImg, (0, 0))

# player
playerImg = pygame.image.load('player.png')
playerX = ScreenX//2 - 32
playerY = ScreenY-96
playerX_change = 5

def player(x, y):
    screen.blit(playerImg, (x, y))

# enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, ScreenX-64)
enemyY = random.randint(64, ScreenY//2 - 64)
enemyX_change = EXchange
enemyY_change = EYchange

def enemy(X, Y):
    screen.blit(enemyImg, (X, Y))

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = BX
bulletY = (ScreenY-96)
bullet_state = "ready"
bulletX_change = BXchange
bulletY_change = BYchange

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# score
score_value = 0
scoreX = 10
scoreY = 10

#gameover
def gameover():
    font = pygame.font.SysFont("DejaVuSans", 64)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (170, ScreenY//2))

def score(score_value, x, y):
    font = pygame.font.SysFont("DejaVuSans", 32)
    text = font.render("Score : " + str(score_value), True, RED)
    screen.blit(text, (x, y))

bullet_value = 0

def bullet_used(bullet_value):
    font = pygame.font.SysFont("DejaVuSans", 32)
    text = font.render("Bullet Used : " + str(bullet_value), True, RED)
    screen.blit(text, (2*ScreenX//3, 10))

efficiency_value = 0

def efficiency(efficiency_value):
    font = pygame.font.SysFont("DejaVuSans", 32)
    text = font.render("Efficiency : " + str(str(efficiency_value)+'%'), True, WHITE)
    screen.blit(text, (ScreenX//3 -48,10))

# collision
def isCollision(bulletX, bulletY, enemyX, enemyY):
    Distance = (math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if Distance < 27:
        return True
    else:
        return False

running = True
touch = False

while running:

    screen.fill((100, 0, 100))
    #background()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_value += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if enemyY > ScreenY//2:
        enemyY = 2*ScreenY
        playerY = 2*ScreenY
        bullet_state = "NULL"
        gameover()
        score(score_value, 270, 500)

    else:
        score(score_value, 10, 10)
        bullet_used(bullet_value)
        if bullet_value > 0:
            efficiency(round((score_value / bullet_value) * 100, 2))

    if playerX <= 0:
        playerX = 0
    elif playerX >= (ScreenX-64):
        playerX = (ScreenX-64)

    if bulletY <= 0:
        bulletY = BY
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 1 #6
        enemyY += enemyY_change
    elif enemyX >= (ScreenX-64):
        enemyX_change = -1 #-6
        enemyY += enemyY_change

    collision = isCollision(bulletX, bulletY, enemyX, enemyY)

    if collision:
        bullet_state = "ready"
        score_value += 1
        bulletY = BY
        enemyX = random.randint(0, ScreenX-64)
        enemyY = random.randint(64, ScreenY//2-64)

    # background()
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
