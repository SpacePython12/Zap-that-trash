import pygame
import random

pygame.init()
pygame.mixer.init()
fire = pygame.mixer.Sound("resources/sounds/fire.wav")
hit = pygame.mixer.Sound("resources/sounds/hit.wav")

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/textures/boat.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = pygame.Surface.get_rect(self.image, center=(512, 464))
        self.motion = 0
        self.bulletlist = []
        self.bulletcooldown = 25
        self.cooldown = self.bulletcooldown

    def update(self, key, mouse):
        self.motion += -self.motion*0.1
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.motion += -0.3
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.motion += 0.3
        if key[pygame.K_SPACE] and self.cooldown >= self.bulletcooldown:
            self.bulletlist.append(Bullet((self.rect.centerx, self.rect.bottom), self.bulletlist))
            fire.play()
            self.cooldown = 0
        self.rect.move_ip(self.motion, 0)
        self.cooldown += 1

class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__()
        self.image = pygame.image.load("resources/textures/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = pygame.Surface.get_rect(self.image, center=pos)
        self.group = group

    def update(self, targetgroup):
        self.rect.move_ip(0, 5)
        collided = pygame.sprite.spritecollideany(self, targetgroup)
        if collided and not collided.dead:
            hit.play()
            if type(collided) is Trash:
                collided.die()
                self.group.remove(self)
                return 3
            elif type(collided) is Fish:
                collided.die()
                self.group.remove(self)
                return -5
        else:
            if self.rect.y > 720:
                self.group.remove(self)
            return 0

        
class Trash(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 2)
        self.image = pygame.image.load(f"resources/textures/trash{self.type}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image = pygame.transform.rotate(self.image, random.randint(-180, 180))
        self.startpos = (0, random.randint(600, 700))
        self.rect = pygame.Surface.get_rect(self.image, center=self.startpos)
        self.dead = False
        self.deadfor = 0

    def update(self, speed):
        self.rect.move_ip(1*speed, 0)
        if self.rect.x > 1024:
            self.kill()
        if self.dead:
            if self.deadfor == 10:
                self.kill()
            else:
                self.deadfor += 1
    
    def die(self):
        self.dead = True
        self.image = pygame.image.load(f"resources/textures/pop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

class Fish(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.type = random.randint(0, 2)
        self.image = pygame.image.load(f"resources/textures/fish.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.startpos = (0, random.randint(600, 700))
        self.rect = pygame.Surface.get_rect(self.image, center=self.startpos)
        self.dead = False
        self.deadfor = 0

    def update(self, speed):
        self.rect.move_ip(1*speed, 0)
        if self.rect.x > 1024:
            self.kill()     
        if self.dead:
            if self.deadfor == 10:
                self.kill()
            else:
                self.deadfor += 1

    def die(self):
        self.dead = True
        self.image = pygame.image.load(f"resources/textures/pop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))