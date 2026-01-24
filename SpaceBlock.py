import pygame
import sys
from math import sqrt
from random import randint
from time import sleep,time
color={"red":(255,0,0),"green":(0,255,0),"white":(255,255,255),"black":(0,0,0)}

class Vector:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def __add__(self,value):
        if(isinstance(value,Vector)):
            return Vector(self.x+value.x,self.y+value.y)
        elif(isinstance(value,(int,float))):
            return Vector(self.x+value,self.y+value)
        else:
            raise ValueError(f"not {type(value)} Value")
    def __sub__(self,value):
        if(isinstance(value,Vector)):
            return Vector(self.x-value.x,self.y-value.y)
        elif(isinstance(value,(int,float))):
            return Vector(self.x-value,self.y-value)
        else:
            raise ValueError(f"not {type(value)} Value")
    def __truediv__(self,value):
        if(isinstance(value,Vector)):
            return Vector(self.x/value.x,self.y/value.y)
        elif(isinstance(value,(int,float))):
           return  Vector(self.x/value,self.y/value)
        else:
          raise ValueError(f"not {type(value)} Value")
    def __mul__(self,value):
        if(isinstance(value,Vector)):
            return Vector(self.x*value.x,self.y*value.y)
        elif(isinstance(value,(int,float))):
            return Vector(self.x*value,self.y*value)
        else:
            raise ValueError(f"not {type(value)} Value")
    def __str__(self):
        return f"<vector {self.x} {self.y} >"
    def length(self):
        return sqrt(self.x**2+self.y**2)
    def null(self):
        return self.x==0 and self.y==0
    def normalized(self):
        return self/self.length()
class Player(pygame.Rect):
    def __init__(self,position,size,speed):
        super().__init__(position[0],position[1],size,size)
        self.speed=speed 
    def add(self,velocity):
        if(velocity.null()):
            return
        velocity=velocity.normalized()*self.speed
        self.x+=velocity.x
        self.y+=velocity.y
        self.x%=600
        self.y%=600
class Ennemy(pygame.Rect):
    def __init__(self,size,speed):
        super().__init__([0,0],[size,size])
        cote=randint(0,3) 
        if(cote==0):#top
            self.position=Vector(randint(100,500),0)
            self.end=Vector(randint(100,500),600)
        elif(cote==1):#left
            self.position=Vector(600,randint(100,500))
            self.end=Vector(0,randint(100,500)) 
        elif(cote==2): #bottom
            self.position=Vector(randint(100,500),600)
            self.end=Vector(randint(100,500),0)
        elif(cote==3):#rigth
            self.position=Vector(0,randint(100,500))
            self.end=Vector(600,randint(100,500))
        self.velocity=(self.end-self.position).normalized()*speed
    def steep(self):
        self.position=self.position+self.velocity
        self.x=round(self.position.x)
        self.y=round(self.position.y)
        
class Coin(pygame.Rect):
    def __init__(self,rare):
        self.rare=rare
        if(rare):
            size=25
        else:
            size=30
        super().__init__([randint(100,500),randint(100,500)],[size,size]) 
        self.color=[randint(0,255),randint(0,255),randint(0,255)]




class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Block")
        self.window=pygame.display.set_mode((600,600))
        self.font=pygame.font.SysFont("arial",20,True)
        self.clock=pygame.time.Clock()
        self.higthscore=0
        self.running=True
        if(len(sys.argv)>1 and sys.argv[1]=="-DEBUG"):
            self.DEBUG=True
        else:
            self.DEBUG=False
        while(self.running):
           self.chrono=time()
           self.player=Player([300,300],25,13)
           self.coins=[]
           self.ennemys=[]
           self.score=0
           self.MODE={"speedBlock":3,"sizeBlock":75,"numberBlock":1,"numberCoin":1}
           self.update()
           sleep(0.1)
        
    def update(self):
        while(True):
            self.window.fill(color["black"])
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.running=False
                    return
            self.clock.tick(30)
            self.Spawn()
            self.CheckcollisionCoin()
            if(self.CheckcollisionEnnemy()):
                break
            velocity=Vector(0,0)
            keys=pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                    velocity.y-=1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    velocity.y+=1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    velocity.x+=1
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                    velocity.x-=1
            self.player.add(velocity)
            self.TextRender()
            pygame.draw.rect(self.window,color["white"],self.player,5)
            pygame.display.flip()
    def CheckcollisionCoin(self):
      for coin in self.coins:
        if(self.player.colliderect(coin)):
            if(coin.rare):
             self.score+=3
            else:
             self.score+=1
            if(self.score>self.higthscore):
                self.higthscore=self.score
            self.SetDifficulty()
            self.coins.remove(coin)
            continue
        if(self.DEBUG):
            pygame.draw.rect(self.window,color["green"],coin)
        if(coin.rare):
            coin.color[0]+=randint(50,60)
            coin.color[1]+=randint(50,60)
            coin.color[2]+=randint(50,60)
            coin.color[0]%=256
            coin.color[1]%=256
            coin.color[2]%=256
            pygame.draw.circle(self.window,coin.color,coin.center,coin.width/2)
        else:
            pygame.draw.circle(self.window,coin.color,coin.center,coin.width/2,5)
    def TextRender(self):
           self.window.blit(self.font.render(f"Score : {self.score}",True,color["white"] ),[10,10])
           self.window.blit(self.font.render(f"HigthScore : {self.higthscore}",True,color["white"] ),[10,30])
           self.window.blit(self.font.render(f"Time : {round(time()-self.chrono,1)}",True,color["white"]),[450,10])
          
    def CheckcollisionEnnemy(self):
      for ennemy in self.ennemys:
            if(self.player.colliderect(ennemy)):
                return True
            ennemy.steep()
            if(ennemy.center[0]>600 or ennemy.center[0]<0 or ennemy.center[1]>600 or ennemy.center[1]<0):
                self.ennemys.remove(ennemy)
                continue
            if(self.DEBUG):
                pygame.draw.line(self.window,color["green"],[ennemy.position.x,ennemy.position.y],[ennemy.end.x,ennemy.end.y])
            pygame.draw.rect(self.window,color["red"],ennemy,5)
      return False
    def SetDifficulty(self):
        if(self.score<10):
            self.MODE["speedBlock"]=3
            self.MODE["numberBlock"]=3
            self.MODE["sizeBlock"]=50
            self.MODE["numberCoin"]=1
        elif(self.score>10 and self.score<30):
            self.MODE["speedBlock"]=5
            self.MODE["numberBlock"]=3
            self.MODE["sizeBlock"]=40
            self.MODE["numberCoin"]=3
        elif(self.score>30 and self.score<50):
            self.MODE["speedBlock"]=7
            self.MODE["numberBlock"]=3
            self.MODE["sizeBlock"]=40
            self.MODE["numberCoin"]=5
        elif(self.score>50):
            self.MODE["speedBlock"]=9
            self.MODE["numberBlock"]=3
            self.MODE["sizeBlock"]=40
            self.MODE["numberCoin"]=7
         
    def Spawn(self):
        if(len(self.ennemys)<self.MODE["numberBlock"]):
            self.ennemys.append(Ennemy(self.MODE["sizeBlock"],self.MODE["speedBlock"]))
        if(len(self.coins)<self.MODE["numberCoin"]):
            self.coins.append(Coin(randint(1,5)==1))
           
   
       
Game()
        
