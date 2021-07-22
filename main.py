import pygame
import random
pygame.init()

sw = 800
sh = 800
back = pygame.image.load("background.jpeg")

win = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

gameover = False

class Paddle(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.xx = self.x + self.w
        self.yy = self.y + self.h
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,[self.x,self.y,self.w,self.h])

class Ball(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.xv = random.choice([2,3,4,-2,-3,-4])
        self.yv = random.randint(3,4)
        self.xx = self.x + self.w
        self.yy = self.y + self.h        

    def draw(self,win):
        pygame.draw.rect(win,self.color,[self.x,self.y,self.w,self.h])
    
    def move(self):
        self.x+= self.xv
        self.y+=self.yv

class Brick(object):
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.yy = self.y + self.h

    def draw(self,win):
        pygame.draw.rect(win,self.color,[self.x,self.y,self.w,self.h])
        
bricks = []        
def init():
    global bricks
    bricks = []
    for i in range(6):
        for j in range(10):
            bricks.append(Brick(10+j*79,50+i*35,70,25,(120,205,250)))

def reGW():
    win.blit(back, (0,0))
    player.draw(win)
    ball.draw(win)
    for b in bricks:
        b.draw(win)
    font = pygame.font.SysFont("comicsans",50)
    if gameover:
        if len(bricks)==0:
            resText = font.render("You WIN!!",1,(255,255,255))
        else:
            resText = font.render("Try Again, press space to continoe",1,(255,225,225))
        win.blit(resText,((sw//2-resText.get_width()//2),sh//2 - resText.get_height()//2))
        playAgainText = font.render("Press Space To Play Again",1,(255,255,255))
        win.blit(playAgainText,sw)
    pygame.display.update()

player = Paddle(sw/2-50,sh-100,100,20,(255,255,255))
ball = Ball(sw/2-10,sh-200,20,20,(255,255,255))
init()
run = True
while run:
    clock.tick(100)
    if not gameover:
        ball.move()
        if pygame.mouse.get_pos()[0] - player.w/2<0:
            player.x=0
        elif pygame.mouse.get_pos()[0] + player.w/2>sw:
            player.x = sw - player.w
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w//2


        if (ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
            if ball.y + ball.h >= player.y and ball.h <= player.y + player.h:
                ball.yv *=-1

        if ball.x + ball.w >= sw:
            ball.xv *= -1
        if ball.x < 0:
            ball.xv *= -1
        if ball.y <= 0:
            ball.yv *= -1

    for brick in bricks:
        if(ball.x >= brick.x and ball.x <= brick.x + brick.w) or ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w:
            if (ball.y >= brick.y and ball.y <= brick.y + brick.h) or ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y +brick.h:
                brick.visible = False
                bricks.pop(bricks.index(brick))
                ball.yv*=-1 

    if ball.y> sh:
        gameover = True


    keys = pygame.key.get_pressed()
    if len(bricks) == 0:
        won =True
        gameover = True
    if gameover:
        if keys[pygame.K_SPACE]:
            gameover = False
            won = False
            ball = Ball(sw/2-10,sh-400,20,20,(225,225,225))
            bricks.clear()
            init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    reGW()
pygame.quit()