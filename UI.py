import pygame

from Animation import ImageAnimation

class Button(ImageAnimation):
    def __init__(self,position,surface,size,AnimationTime):
        super().__init__(position,surface,"scale",size,AnimationTime)
    def update(self,delta):
        super().update(delta,self.is_focus())
    def is_focus(self):
       RectMousse=pygame.rect.Rect(pygame.mouse.get_pos(),(1,1))
       return self.rect.colliderect(RectMousse)
    def is_click(self):
        return self.is_focus() and pygame.mouse.get_pressed()[0]

        
class Key(ImageAnimation):
    def __init__(self,position,OFF,ON):
        super().__init__(position,OFF,"scale",(1,1.05),0.5)
        self.ON=ON
        self.OFF=OFF
        self.value=False
    def update(self,delta):
        if(self.value):
            self.surface=self.ON
        else:
           self.surface=self.OFF
        super().update(delta,self.value)
       