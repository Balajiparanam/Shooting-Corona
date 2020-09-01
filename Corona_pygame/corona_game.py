import pygame
import random
pygame.init()
w = 400
h = 600
pygame.mixer.init()
win = pygame.display.set_mode((400, 600))
pygame.display.set_caption('Corona Game')
font = pygame.font.SysFont('comicsans', 40)
background = pygame.image.load('background5.jpg')
different_viruses = [pygame.image.load('{0}_Virus.png'.format(colors)) for colors in ['Red', 'Blue', 'Green', 'Pink', 'Yellow']]
score = 0
run = True

clock = pygame.time.Clock()
class perso(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('stand2.jpg'), (34, 54))
        self.image.set_colorkey((255,255,255))

        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.centerx = w//2
        self.rect.bottom = h-10
        self.speed = 8
        self.health = 50
        

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x -=self.speed

        if keystate[pygame.K_RIGHT] and self.rect.right<w:
            self.rect.x+=self.speed

    def shoot(self):
        bullet = bullets(self.rect.centerx, self.rect.top)
        sprites.add(bullet)
        Bullets.add(bullet)


        
def player_health(win,x, y, health):
    if health<0:
        health = 0
    pygame.draw.rect(win, (255,255,255),(x,y, 100,10), 2)
    pygame.draw.rect(win, (0,255,0), (x,y, (health/50)*100,10))


class ene(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(different_viruses)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)
        self.rect.x = random.randrange(0,w-self.rect.width)
        self.rect.y = random.randrange(-50,-10 )
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-1,1)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now-self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot+self.rot_speed)%360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            

    def update(self):
        self.rotate()
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>h or self.rect.left<-10 or self.rect.right>w+20:
            self.rect.x = random.randrange(0,w-self.rect.width)
            self.rect.y = random.randrange(-10, 0)
            self.speedy = random.randrange(1,8)


class bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.transform.scale(pygame.image.load('bullet.png'),(10,30))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed= -10

    def update(self):
        self.rect.y+=self.speed
        if self.rect.bottom<0:
            self.kill()
        
def game_over():
    win.blit(background, (0,0))
    text1 = font.render('Game Over', 1, (255, 255,255))
    win.blit(text1, (w//2-(text1.get_width()//2), h/2))
    font2 = pygame.font.SysFont('comicsans', 20)
    text3 = font2.render('ARROW Keys for movement and SPACE to Fire',1, (255, 255,255))
    win.blit(text3, (w//2-(text3.get_width()//2), h/4))
    text2 = font2.render('Press any key to begin' , 1, (255, 255, 255))
    win.blit(text2, (w//2-(text2.get_width()//2), 3*h/4))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
pygame.mixer.music.load('music.mp3')
    
person = perso()

Bullets = pygame.sprite.Group()
sprites = pygame.sprite.Group()
sprites.add(person)

enemy_sprit = pygame.sprite.Group()
for i in range(5):
    enemy = ene()
    sprites.add(enemy)
    enemy_sprit.add(enemy)
pygame.mixer.music.play(-1)
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                person.shoot()

    hits = pygame.sprite.groupcollide(enemy_sprit, Bullets, True, True)
    for hit in hits:
        enemy = ene()
        enemy_sprit.add(enemy)
        sprites.add(enemy)
        score +=10
    damage = pygame.sprite.spritecollide(person, enemy_sprit, True, pygame.sprite.collide_circle)
    for dam in damage:
        enemy = ene()
        enemy_sprit.add(enemy)
        sprites.add(enemy)
        person.health-=5
        if person.health<=0:
            game_over()
        
        
    win.blit(background, (0,0))
    sprites.update()
    sprites.draw(win)
    player_health(win, 60,4,person.health)
    text1 = font.render('Score: ' +str(score), 1, (255, 255, 255))
    win.blit(text1, (250, 0))
    font2 = pygame.font.SysFont('comicsans', 25)
    text2 = font2.render('Player: ', 1, (255, 255, 255))
    win.blit(text2, (0,0))
    pygame.display.update()

pygame.quit()


    

