import pygame
import random
import json
import math
from sprites import *

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("resources/sounds/music.wav")
SHEIGHT = 720
SWIDTH = 1024
display = pygame.display.set_mode((SWIDTH, SHEIGHT))
clock = pygame.time.Clock()
data = json.loads(open("resources/data.json").read())
pygame.display.set_caption("Zap that trash!")
icon = pygame.image.load("resources/textures/boat.png").convert_alpha()
pygame.display.set_icon(icon)
drawgroup = pygame.sprite.Group()
player = Player()
drawgroup.add(player)
currenttick = 0
targetgroup = pygame.sprite.Group()
score = 20
highscore = data["highscore"]
deathtimer = 0
pygame.mixer.music.play(loops=99999)
running = True
while running:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if score > 0:
        currenttick += 1
        if currenttick % 50 == 0:
            for c in range(1):
                if random.randint(0, 3) == 0:
                    fish = Fish()
                    drawgroup.add(fish)
                    targetgroup.add(fish)
                else:
                    trash = Trash()
                    drawgroup.add(trash)
                    targetgroup.add(trash)
        display.fill((0, 127, 255))
        pygame.draw.rect(display, (49, 0, 255), pygame.Rect(0, 480, 1024, 240))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.x = 0
        textRect.y = 0
        text2 = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
        textRect2 = text2.get_rect()
        textRect2.x = 0
        textRect2.y = 32
        tut = font.render(f"Hit the plastic and avoid the fish!", True, (255, 255, 255))
        tutRect = tut.get_rect()
        tutRect.right = SWIDTH
        tutRect.y = 0
        display.blit(text, textRect)
        display.blit(text2, textRect2)
        display.blit(tut, tutRect)
        if score > highscore:
            highscore = score
        player.update(pygame.key.get_pressed(), pygame.mouse.get_pressed())
        for bullet in player.bulletlist:
            display.blit(bullet.image, bullet.rect)
            score += bullet.update(targetgroup)
        targetgroup.update(math.sqrt(score)/4)
        drawgroup.draw(display)
    else:
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            score = 20
            deathtimer = 0
            pygame.mixer.music.unpause()
        if deathtimer == 1:
            pygame.mixer.music.pause()
        else:
            deathtimer += 1
        display.fill((0, 0, 0))
        text = font.render(f"Game Over", True, (255, 0, 0))
        textRect = text.get_rect()
        textRect.center = (int(SWIDTH/2), int(SHEIGHT/2))
        display.blit(text, textRect)
        text2 = font.render(f"Press enter to restart", True, (255, 0, 0))
        textRect2 = text2.get_rect()
        textRect2.center = (int(SWIDTH/2), int(SHEIGHT/2)+32)
        display.blit(text2, textRect2)
    pygame.display.update()
data["highscore"] = highscore
open("resources/data.json", "w").write(json.dumps(data))