import pygame
class ImageAnimation:
    def __init__(self,position,surface,name,size,AnimationTime):
        self.surface=surface
        self.image=surface
        self.position=position
        self.rect=surface.get_rect(center=self.position)
        self.size=size
        self.name=name
        self.AnimationTime=AnimationTime
        self.time=0
        
    def update(self,delta,state):
       if(state):
           self.time+=delta
           self.time=min(self.time,self.AnimationTime)
       else:
           self.time-=delta
           self.time=max(0,self.time)
       factor=self.size[0]+(self.size[1]-self.size[0])*(self.time/self.AnimationTime)
       self.Animate(factor)
       
    def Animate(self,factor):
       if self.name=="transparency":
            self.image.set_alpha(factor)
       elif self.name=="scale":
            self.image=pygame.transform.scale_by(self.surface,factor)
       elif self.name=="rotate":
            self.image=pygame.transform.rotate(self.surface,factor)
       self.rect=self.image.get_rect(center=self.position)
     
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        