import pygame, random, time, os.path
from pygame.locals import *
pygame.mixer.init()
pygame.init()

# setting up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)
MAGENTA = (200, 0 ,200)
SKYBLUE = (135, 206, 250)

# setting up the  screen
flag = RESIZABLE
SCREEN = pygame.display.set_mode((800,600),flag)
pygame.display.set_caption('Jet_Game')
Icon = pygame.transform.scale(
    pygame.image.load(os.path.join('images','jet1.png')), (64,64)
)
pygame.display.set_icon(Icon)
screen = SCREEN.get_rect()
screen_width,screen_height = screen.size
swc, shc = screen.center    #screen width center, screen height center
background = SKYBLUE

# setting up the clock
clock = pygame.time.Clock()
# initialize explosion animation sprite
anim_list = []
for i in range(0,9):
    name = 'images{}explosion{}regularExplosion0{}.png'.format(os.path.sep,os.path.sep,i)
    surface = pygame.transform.scale(pygame.image.load(name),(100,100))
    anim_list.append(surface)
class Explosion(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Explosion, self).__init__()
        self.anim_list = anim_list
        self.surf = self.anim_list[0]
        self.rect = self.surf.get_rect(center=pos)
        self.frame = 0
        self.frame_rate = 100
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.anim_list):
                self.kill()
            else:
                self.surf = self.anim_list[self.frame]
                self.rect = self.surf.get_rect(center=self.rect.center)

    ### initializing sounds : TO-DO
#up_sound = pygame.mixer.Sound(os.path.join('music','sound.ogg'))
#down_sound = pygame.mixer.Sound(os.path.join('music','sound.ogg'))
#collision_sound = pygame.mixer.Sound(os.path.join('music','sound.ogg'))
#game_over_sound = pygame.mixer.Sound(os.path.join('music','sound.ogg'))


''' gui text printer function'''
def Print(text,my_font,size,pos,color,surface):
    if my_font == "None":
        font = pygame.font.SysFont(None,size)
    else:
        font = pygame.font.Font(my_font,size)
    surf = font.render(text,True,color)
    rect = surf.get_rect(center=pos)
    surface.blit(surf,rect)

''' intro screen '''
def intro():
    global flag, SCREEN, screen, screen_width, screen_height, swc, shc
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return False
            if event.type == VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, flag)
                screen = SCREEN.get_rect()
                screen_width, screen_height = screen.size
                swc, shc = screen.center
        SCREEN.fill(SKYBLUE)
        txt1 = '''Special credit to the providers of the free images, at www.kenney.nl'''
        txt2 = '''This game was developed by @K-Kelvin, a fullstack developer'''
        surf = pygame.Surface((swc + 300, shc))
        surf.fill(GRAY)
        rect = surf.get_rect(center=(swc, shc))
        SCREEN.blit(surf, rect)
        Print("Jet Game", "font/font_menu.ttf", 75, (swc, shc - 50), RED, SCREEN)
        Print("Author: @K-Kelvin", None, 50, (swc, shc + 20), WHITE, SCREEN)
        Print(txt1, None, 30, (swc, shc + 60), WHITE, SCREEN)
        Print(txt2, None, 30, (swc, shc + 90), WHITE, SCREEN)
        Print("Press any key to go back...", None, 30, (swc, screen_height - 50), RED, SCREEN)
        pygame.display.update()

''' pause the game '''
def pause():
    global flag, SCREEN, screen, screen_width, screen_height, swc, shc
    Print("Paused", None, 80, (swc, shc), RED, SCREEN)
    pygame.display.flip()
    time.sleep(0.5)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, flag)
                screen = SCREEN.get_rect()
                screen_width, screen_height = screen.size
                swc, shc = screen.center
            if event.type == KEYDOWN:
                if event.key == K_p:
                    box = Rect(0,0,swc//2,shc//4)
                    box.center = swc,shc
                    pygame.draw.rect(SCREEN, RED,box)
                    Print("Play", None, 80, (swc, shc), WHITE, SCREEN)
                    pygame.display.flip()
                    time.sleep(0.2)
                    return False
        time.sleep(0.1)

''' save and load the high score '''
def HighScore():
    global score, high_score
    if not os.path.exists(os.path.join(os.path.dirname(__file__),'db')):
        os.mkdir('db')
    name = os.path.join('db','high_score.txt')
    try:
        file = open(name,"r")
        high_score = file.read()
    except:
        new = open(name,"w")
        new.write(str(score))
        new.close()
        file = open(name,"r")
        high_score = file.read()
    if int(score) > int(high_score):
        high_score = str(score)
        o = open(name,"w")
        o.write(high_score)
    return high_score

''' reset the high score '''
def Reset():
    global high_score
    path = os.path.join('db','high_score.txt')
    file = open(path,"w")
    file.write("0")
    file.close()
    r = open(path,"r")
    high_score = r.read()

''' the main loop for playing the game'''
def main():
    enemy_speed = 1
    ''' creating the player attributes/properties '''
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load(os.path.join('images','jet1.png')).convert()
            self.surf.set_colorkey(BLACK)
            self.rect = self.surf.get_rect(left = 80, top = 200)
            self.radius = int(self.rect.height*0.8//2)

        # move player within the screen boundary
        def update(self):
            speed = 10
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT] and self.rect.left > 0:
                self.rect.move_ip(-speed, 0)
            if pressed_keys[K_RIGHT] and self.rect.right < screen_width-5:
                self.rect.move_ip(speed, 0)
            if pressed_keys[K_UP] and self.rect.top > 0:
                self.rect.move_ip(0, -speed)
            if pressed_keys[K_DOWN] and self.rect.bottom < screen_height-5:
                self.rect.move_ip(0, speed)
            pygame.display.update()
    player = Player()

    ''' creating the enemy attributes/properties '''
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            m = random.randint(1,8)
            self.surf = pygame.image.load("images{}missile{}.png".format(os.path.sep,str(m))).convert()
            self.surf.set_colorkey(BLACK)
            self.rect = self.surf.get_rect(
                    center = (random.randint(screen_width+100,screen_width+110),random.randint(10,screen_height-10))
            )
            self.radius = int(self.rect.height//2)
            self.speed = random.randint(15,20)

        def update(self):
            self.rect.move_ip(-self.speed,0)
            if self.rect.right < 0:
                self.kill()
        pygame.display.update()
    enemy = Enemy()

    ''' creating the cloud attributes/properties '''
    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            num = random.randint(1,8)
            self.surf = pygame.image.load("images{}cloud{}.png".format(os.path.sep,str(num))).convert()
            self.surf.set_colorkey(BLACK)
            self.rect = self.surf.get_rect(
                    center = (random.randint(screen_width+100,screen_width+200),random.randint(10,screen_height))
            )
            self.speed = random.randint(8,12)

        def update(self):
            self.rect.move_ip(-self.speed,0)
            if self.rect.right < 0:
                self.kill()
        pygame.display.update()
    cloud = Cloud()

    ''' Group sprites to hold multiple objects '''
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    the_player = pygame.sprite.Group()
    explosion = pygame.sprite.Group()
    the_player.add(player)

    ''' Custom events : loop to set timer for objects generation '''
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 500)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)
    ADDSCORE = pygame.USEREVENT + 3
    pygame.time.set_timer(ADDSCORE, 100)
    INCREMENT_SPEED = pygame.USEREVENT + 4
    pygame.time.set_timer(INCREMENT_SPEED, 5000)

    ''' Function to initialize and update the score to the screen '''
    def SCORE():
        font = pygame.font.SysFont(None,24)
        my_score = font.render("SCORE: {0}".format(str(score)),True,BLACK)
        SCREEN.blit(my_score,(10,10,100,100))

    def music(opt='play'):
        # background music
        if opt == 'play':
            pygame.mixer.music.load("music{}511508__greek555__loop-mix.mp3".format(os.path.sep))
            pygame.mixer.music.play(loops=-1)
        elif opt == 'stop':
            pygame.mixer.music.stop()

    background_dict = {0:SKYBLUE,1:GRAY,2:MAGENTA,3:BLACK,4:GREEN}
    background = background_dict[0]
    global score,SCREEN,screen,screen_width,screen_height,swc,shc
    count = 1
    running = True
    music()
    while running:
        ''' check for events in the queue '''
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, flag)
                screen = SCREEN.get_rect()
                screen_width, screen_height = screen.size
                swc, shc = screen.center
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    pause()
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_LSHIFT:
                    background = SKYBLUE
                if event.key == K_RSHIFT:
                    background = background_dict[random.randint(1,len(background_dict)-1)]
                if event.key == K_r:
                    score = 0
                    main()
                if event.key == K_n:
                    music()
                if event.key == K_m:
                    music('stop')
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                new_enemy.speed += enemy_speed
                enemies.add(new_enemy)
            elif event.type == INCREMENT_SPEED:
                if player in the_player:
                    enemy_speed += 1
            elif event.type == ADDCLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
            elif event.type == ADDSCORE:
                if player in the_player:
                    score+=1
                    pygame.display.update()

        # control player and enemy movements
        the_player.update()
        clouds.update();cloud.update()
        enemies.update();enemy.update()

        SCREEN.fill(background)
        '''drawing all sprites to the screen'''
        for entity in clouds:
            SCREEN.blit(entity.surf,entity.rect)
        for entity in enemies:
            SCREEN.blit(entity.surf,entity.rect)
        for entity in the_player:
            SCREEN.blit(entity.surf,entity.rect)
        ''' single collision between the player and missiles'''
        if count == 1:
            if pygame.sprite.spritecollide(player, enemies,True,pygame.sprite.collide_circle):
                global over, list, selected
                over = True
                list = {**list, **{1: "Restart"}} ; selected = list[1]
                over_time =pygame.time.get_ticks()
                # play explosion sound
                explosion.add(Explosion(player.rect.center))
                player.kill()
                the_player.add(explosion)
                count = 0
        if player not in the_player:
            if pygame.time.get_ticks() - over_time > 1000:
                running = False
        SCORE()
        pygame.display.flip()
        clock.tick(40)
    music('stop')
    start_menu()


score = 0
over = False
list = {1:"Start",2:"About",3:"High Score",4:"Quit"} ; selected = list[1]
HighScore() # initialize the high_score
def start_menu():
    global over, list, selected, flag,SCREEN,screen,screen_width,screen_height,swc,shc
    start_menu = True
    j = 1
    while start_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == VIDEORESIZE:
                SCREEN = pygame.display.set_mode(event.size, flag)
                screen = SCREEN.get_rect()
                screen_width, screen_height = screen.size
                swc, shc = screen.center
            if event.type == KEYDOWN:
                # toggle through the menu list
                if event.key == K_UP:
                    if j > 1:
                        j -= 1
                    selected = list[j]
                if event.key == K_DOWN:
                    if j < len(list):
                        j += 1
                    selected = list[j]
                # hit enter to selected the menu item
                if event.key == K_RETURN:
                    if selected == list[1]:
                        global score
                        score = 0
                        over = False
                        main()
                    elif selected == "About":
                        intro()
                    elif selected == list[len(list)]:
                        pygame.quit()
                        quit()
        SCREEN.fill(SKYBLUE)
        ## main code goes here
        img = pygame.transform.scale(pygame.image.load("images{}backgroundEmpty.png".format(os.path.sep)).convert(),(screen_width,screen_height))
        img.set_colorkey(BLACK)
        SCREEN.blit(img,(0,0))
        loop = 0
        keys = pygame.key.get_pressed()

        for i in range(1,len(list)+1):
            font = "font{}font_menu.ttf".format(os.path.sep)
            if selected == list[i]:
                Print(list[i].upper(),font,40,(swc,shc+loop),RED,SCREEN)
                if selected == "High Score":
                    Print("   : {}".format(str(high_score)),font,45,(swc+200,shc+loop), RED, SCREEN)
                loop += 50
            else:
                Print(list[i],None,50,(swc,shc+loop),BLACK,SCREEN)
                loop+=50

        if over:
            ''' this will be the point to capture the score and compare it to the high score '''
            if keys[K_r]:
                over = False
            HighScore()# if the score is greater than the high score, overwrite the high score with the score value
            message1 = "GAME OVER!"
            message = "YOUR SCORE: {0}".format(str(score))
            Print(message1,font,50,(swc,shc-200),MAGENTA,SCREEN)
            Print(message,font,50,(swc,shc-150),MAGENTA,SCREEN)

        if keys[K_r]:
            Reset()
        Print("Author : @K-Kelvin",None,30,(swc+300,shc+250),BLACK,SCREEN)
        pygame.display.update()
        clock.tick(40) # 40 frames per second

if __name__ == '__main__':
    try:
        start_menu()
    except KeyboardInterrupt as e:
        print(e,", exiting")
