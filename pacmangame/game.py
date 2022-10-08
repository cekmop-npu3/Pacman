import pygame
import sys
pygame.init()
w=800
h=800
pacx=0
pacy=0
ghostx=0
ghosty=0
fps=60
count=0
br_time=True
point_count=0
bright=0
speed=3
death=False
d=True
sounds=True
walk_sounds=True
pygame.mixer.init()
walking=pygame.mixer.Sound('sounds/walking.wav')
walking.set_volume(0.2)
eating=pygame.mixer.Sound('sounds/eating.wav')
eating.set_volume(0.2)
death1=pygame.mixer.Sound('sounds/death.wav')
death1.set_volume(0.2)
win=pygame.mixer.Sound('sounds/win.wav')
win.set_volume(0.2)
window=pygame.display.set_mode((w,h))
pygame.display.set_caption('pacman')
pygame.time.set_timer(pygame.USEREVENT,1000)
class Heros(pygame.sprite.Sprite):
    def __init__(self,x,y,name):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(name)
        self.rect=self.image.get_rect(topleft=(x*32+3,y*32+3))
class Ghosts(pygame.sprite.Sprite):
    def __init__(self,x,y,name,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(name)
        self.rect=self.image.get_rect(topleft=(x*32,y*32))
        self.dir=dir
        self.recty=((y))
        self.rectx=((x))
    def update(self):
        global map
        if death==False:
            if self.dir==2:
                if self.recty==1:
                    if map[self.rect.y//32+1][self.rect.x//32]!=1:
                        self.rect.y+=3
                    elif map[self.rect.y//32+1][self.rect.x//32]==1 :
                        self.recty=23
                else:
                    if map[self.rect.y//32][self.rect.x//32]!=1:
                        self.rect.y-=3
                    elif map[self.rect.y//32][self.rect.x//32]==1:
                        self.recty=1
            else:
                if self.rectx==1:
                    if map[self.rect.y//32][self.rect.x//32+1]!=1:
                        self.rect.x+=3
                    elif map[self.rect.y//32][self.rect.x//32+1]==1 :
                        self.rectx=23
                else:
                    if map[self.rect.y//32][self.rect.x//32]!=1:
                        self.rect.x-=3
                    elif map[self.rect.y//32][self.rect.x//32]==1:
                        self.rectx=1
class Walls(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('images/wall.png')
        self.rect=self.image.get_rect(topleft=(x*32,y*32))
class Points(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height,pad):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((width,height))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect(x=x*32+pad,y=y*32+pad)
map=[]
mapline=[]
map_level=open('level.txt', 'r')
for line in map_level:
    for num in line.strip():
        mapline.append(int(num))
    map.append(mapline)
    mapline=[]
walls=list()
points=pygame.sprite.Group()
big_points=pygame.sprite.Group()
ghosts=pygame.sprite.Group()
ghosts2=pygame.sprite.Group()
for i in range(25):
    for g in range(25):
        if map[i][g]==4:
            pacx=g
            pacy=i
            pacman=Heros(g,i,'images/pacman1.png')
        elif map[i][g]==1:
            walls.append(Walls(g,i))
        elif map[i][g]==2:
            point_count+=1
            points.add(Points(g,i,10,10,11))
        elif map[i][g]==3:
            ghosts.add(Ghosts(g,i,'images/ghost.png',1))
        elif map[i][g]==5:
            ghosts2.add(Ghosts(g,i,'images/ghost.png',2))
        elif map[i][g]==6:
            point_count += 10
            big_points.add(Points(g,i,16,16,8))
default=((pacman.image))
death_fon=pygame.image.load('images/game over.png')
death_fon_rect=death_fon.get_rect(x=144,y=-512)
victory_fon=pygame.image.load('images/victory.png')
victory_fon_rect=victory_fon.get_rect(x=144,y=-512)
images=[default]
def rotate(angle):
    images.pop()
    pacman.image = pygame.image.load('images/pacman2.png')
    angle = angle
    rotate = pygame.transform.rotate(default, angle)
    images.append(rotate)
def ending(fon,fon_rect,inform,sound):
    global death,sounds
    death = True
    pygame.time.set_timer(pygame.USEREVENT, False)
    window.blit(fon, fon_rect)
    fon_rect.y += 4
    if sounds:
        sound.play()
    sounds=False
    if fon_rect.y > 144:
        fon_rect.y = 144
        pygame.time.wait(1000)
        print(inform)
        sys.exit()
def left():
    global pacx,map,pacman
    pacx -= 1
    pacman.rect.x -= 32
    map[pacman.rect.y // 32][pacman.rect.x // 32 + 1] = 0
    map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
def right():
    global pacx, map, pacman
    pacx += 1
    pacman.rect.x += 32
    map[pacman.rect.y // 32][pacman.rect.x // 32 - 1] = 0
    map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
def up():
    global pacy,map,pacman
    pacy -= 1
    pacman.rect.y -= 32
    map[pacman.rect.y // 32 + 1][pacman.rect.x // 32] = 0
    map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
def down():
    global pacy,map,pacman
    pacy += 1
    pacman.rect.y += 32
    map[pacman.rect.y // 32 - 1][pacman.rect.x // 32] = 0
    map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
clock=pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if death==False:
                if event.key==pygame.K_a:
                    rotate(-180)
                    if pacx > 0 and map[pacy][pacx-1] != 1 and map[pacy][pacx-1] != 2 and map[pacy][pacx-1]!=6:
                        walking.play()
                        left()
                    elif pacx>0 and map[pacy][pacx-1] == 2:
                        eating.play()
                        left()
                    elif pacx>0 and map[pacy][pacx-1]==6:
                        eating.play()
                        left()
                    elif pacx<1 and map[pacman.rect.y // 32][pacman.rect.x // 32]==4:
                        walking.play()
                        pacx=24
                        pacman.rect.x=800-32
                        map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
                elif event.key==pygame.K_d:
                    rotate(0)
                    if pacx<24 and map[pacy][pacx+1]!=1 and map[pacy][pacx+1] != 2 and map[pacy][pacx+1]!=6:
                        walking.play()
                        right()
                    elif pacx<24 and map[pacy][pacx+1] == 2:
                        eating.play()
                        right()
                    elif pacx<24 and map[pacy][pacx+1]==6:
                        eating.play()
                        right()
                    elif pacx>23 and map[pacman.rect.y // 32][pacman.rect.x // 32]==4:
                        walking.play()
                        pacx=0
                        pacman.rect.x=0
                        map[pacman.rect.y // 32][pacman.rect.x // 32] = 4
                if event.key==pygame.K_w:
                    rotate(90)
                    if pacy>0 and map[pacy-1][pacx]!=1 and map[pacy-1][pacx]!=2 and map[pacy-1][pacx]!=6:
                        walking.play()
                        up()
                    elif pacy>0 and map[pacy-1][pacx] == 2:
                        eating.play()
                        up()
                    elif pacy>0 and map[pacy-1][pacx]==6:
                        eating.play()
                        up()
                elif event.key==pygame.K_s:
                    rotate(-90)
                    if pacy<24 and map[pacy+1][pacx]!=1 and map[pacy+1][pacx]!=2 and map[pacy+1][pacx]!=6:
                        walking.play()
                        down()
                    elif pacy<24 and map[pacy+1][pacx] == 2:
                        eating.play()
                        down()
                    elif pacy<24 and map[pacy+1][pacx]==6:
                        eating.play()
                        down()
        elif event.type==pygame.KEYUP:
            pacman.image=images[0]
    window.fill((0,0,0))
    window.blit(pacman.image, pacman.rect)
    points.draw(window)
    for i in big_points:
        if bright!=255 and br_time:
            bright+=1
            i.image.set_alpha(bright)
            window.blit(i.image,i.rect)
        else:
            br_time=False
            bright-=1
            if bright==0:
                br_time=True
            i.image.set_alpha(bright)
            window.blit(i.image, i.rect)
            continue
    ghosts.draw(window)
    ghosts2.draw(window)
    ghosts.update()
    ghosts2.update()
    for i in walls:
        window.blit(i.image,i.rect)
    hit1 = pygame.sprite.spritecollide(pacman, points, True)
    if hit1:
        count+=1
        print('you earned ',count,'coins')
    hit=pygame.sprite.spritecollide(pacman,big_points,True)
    if hit:
        count+=10
        print('you earned ',count,'coins')
    if count==point_count:
        ending(victory_fon,victory_fon_rect,f'you earned all {count} points',win)
    hit2=pygame.sprite.spritecollide(pacman,ghosts,False)
    if hit2:
        ending(death_fon,death_fon_rect,f'you have lost and earned {count} coins',death1)
    hit3 = pygame.sprite.spritecollide(pacman, ghosts2, False)
    if hit3:
        ending(death_fon,death_fon_rect,f'you have lost and earned {count} coins',death1)
    pygame.display.update()
    clock.tick(fps)