from math import cos,sin,radians
from random import randint,uniform

import pygame
from pygame import Vector2

class Player(pygame.sprite.Sprite):
   def __init__(self,x,y,surface):
      super().__init__()
      self.FRONT=surface["FRONT.png"].copy()
      self.BACK=surface["BACK.png"].copy()
      self.OFF=surface["OFF.png"].copy()
      self.image=self.OFF
      self.position=Vector2(x,y)
      self.angle=90
      self.speed=450
      self.angularSpeed=350
   def update(self,Input,delta):
      self.move(Input.x,Input.y,delta)
      self.mask=pygame.mask.from_surface(pygame.transform.rotate(self.OFF,self.angle))
      self.rect=self.image.get_rect(center=(round(self.position.x),round(self.position.y)))
   def move(self,x,y,delta):
      if x>0:
         self.angle-=self.angularSpeed*delta
      elif x<0:
         self.angle+=self.angularSpeed*delta
      if y==0:
        self.image=pygame.transform.rotate(self.OFF,self.angle)
        return
      velocity=Vector2(cos(radians(self.angle)),-sin(radians(self.angle)))
      if y<0 :
        velocity*=self.speed
        self.image=pygame.transform.rotate(self.FRONT,self.angle)
      elif y>0 :
        velocity*=-self.speed/2
        self.image=pygame.transform.rotate(self.BACK,self.angle)
    
      self.position+=velocity*delta
      self.position.x%=1280
      self.position.y%=720

class Rock(pygame.sprite.Sprite):
   def __init__(self,speed,surface):
      super().__init__()
      self.image=pygame.transform.rotate(surface[f"{randint(0,11)}.png"].copy(),randint(0,360))
      self.rect=self.image.get_rect()
      self.mask=pygame.mask.from_surface(self.image)
      self.spawn(["top","bottom","left","right"][randint(0,3)],speed)
   def spawn(self,side,speed):
      size=self.image.get_size()
      if side=="top":
         self.position=Vector2(randint(0,1280),-size[0]/2)
         self.end=Vector2(randint(0,1280),720)
      elif side=="bottom":
         self.position=Vector2(randint(0,1280),720)
         self.end=Vector2(randint(0,1280),0)
      elif side=="left":
         self.position=Vector2(0,randint(0,720))
         self.end=Vector2(1280,randint(0,720))
      elif side=="right":
         self.position=Vector2(1280,randint(0,720))
         self.end=Vector2(-size[1]/2,randint(0,720))
      self.velocity=(self.end-self.position).normalize()*speed
   def update(self,delta):
      self.position+=self.velocity*delta
      self.rect.center=(round(self.position.x),round(self.position.y))
    

class Star():
   def __init__(self,surface):
      self.surface=surface
      self.position=(randint(0,1280),randint(0,720))
      self.transform((randint(0,255),randint(0,255),randint(0,255),randint(150,255)),uniform(1,6))
      
   def transform(self,color,length):
      size=self.surface.get_size()
      for x in range(0,size[0]):
         for y in range(0,size[1]):
           r,g,b,alpha=self.surface.get_at((x,y))
           if(alpha==255):
            self.surface.set_at((x,y),color)
      self.surface=pygame.transform.rotate(self.surface,randint(0,360))
      self.surface=pygame.transform.scale_by(self.surface,length)
     
   def draw(self,surface):
      surface.blit(self.surface,self.position)

   
