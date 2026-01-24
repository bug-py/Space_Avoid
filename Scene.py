import sys
from random import randint

import pygame

from Animation import ImageAnimation
import Entity
import UI


class Scene:
   def __init__(self,window,fps):
      self.window=window
      self.fps=fps
      self.transition=ImageAnimation((640,360),pygame.surface.Surface((1280,720)),"transparency",(255,0),0.5)
      
   def start(self):
      clock=pygame.time.Clock()
      while(True):
         for event in pygame.event.get():
            if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
               sys.exit(0)   
         delta=clock.tick(self.fps)/1000
         result=self.process(delta)
         if(result!=None):
               return result
         self.render()
         if(self.transition.time!=self.transition.AnimationTime):
            self.transition.update(delta,True)
            self.transition.draw(self.window)
         pygame.display.flip()
   def process(self,delta):
      pass
   def render(self):
      self.window.fill((0,0,0))
class MainScene(Scene):
   def __init__(self,window,asset,fps):
     self.RectScreen=window.get_rect().inflate(100,100)
     self.rock=pygame.sprite.Group()
     self.player=Entity.Player(640,360,asset["Image"]["ROCKET"])
     image=pygame.transform.rotate(asset["Image"]["ROCKET"]["EXPLOSION.png"].copy(),randint(0,360))
     self.explosion=ImageAnimation((0,0),image,"scale",(1,5),0.8)
     self.sound=asset["Sound"]["Explosion.mp3"]
     self.ROCK_SURFACE=asset["Image"]["ROCK"]
     self.wait=False
     self.score=0
     self.stars=[]
     for _ in range(0,randint(100,150)):
         self.stars.append(Entity.Star(asset["Image"]["STAR.png"].copy()))
     
     super().__init__(window,fps)
   def GetVelocity(self):
      velocity=pygame.Vector2(0,0)
      keys=pygame.key.get_pressed()
      if keys[pygame.K_UP] or keys[pygame.K_z]:
                    velocity.y-=1
      if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    velocity.y+=1
      if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    velocity.x+=1
      if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                    velocity.x-=1
      return velocity
   def process(self,delta):
      if(self.wait):
           self.explosion.update(delta,True)
           if(self.explosion.time==self.explosion.AnimationTime):
                 return self.score
           return 
      difficulty=min((self.score//2)+2,5)
      while(len(self.rock.sprites())!=difficulty):
         self.rock.add(Entity.Rock(170+min(self.score,40),self.ROCK_SURFACE))
        
      self.player.update(self.GetVelocity(),delta)
      self.rock.update(delta)
      self.CheckCollisions()
      
       
   def CheckCollisions(self):
      for sprite in self.rock.sprites().copy():
        result=pygame.sprite.collide_mask(sprite,self.player)
        if(result!=None):   
               impact=(sprite.rect.x+result[0],sprite.rect.y+result[1])
               self.explosion.position=impact
               self.explosion.rect.center=impact
               self.sound.play()
               self.wait=True
        if not sprite.rect.colliderect(self.RectScreen):
              self.rock.remove(sprite)
              self.score+=1 
   def render(self):
      
      if(self.wait):
           self.window.blit(self.explosion.image,self.explosion.rect)
      else:
           self.window.fill((15,15,15))
           for star in self.stars:
             star.draw(self.window)
           self.rock.draw(self.window)
           self.window.blit(self.player.image,self.player.rect)
    
class MenuScene(Scene):
     def __init__(self,window,asset,fps):
        
          self.stars=[]
          for _ in range(0,randint(100,150)):
            self.stars.append(Entity.Star(asset["Image"]["STAR.png"].copy()))
          self.title=UI.Button((650,150),asset["Image"]["UI"]["TITLE.png"],(1,1.2),0.5)
          self.play=UI.Button((650,400),asset["Image"]["UI"]["PLAY.png"],(1,1.5),0.5)
          self.tuto=UI.Button((650,600),asset["Image"]["UI"]["TUTO.png"],(1,1.5),0.5)
          super().__init__(window,fps)
     def process(self, delta):
          self.title.update(delta)
          self.play.update(delta)
          self.tuto.update(delta)
          if(self.play.is_click()):
                return "PLAY"
          if(self.tuto.is_click()):
                return "TUTO"
          if(self.title.is_click()):
               return "MENU"
          
        
     def render(self):
          self.window.fill((15,15,15))
          for star in self.stars:
            star.draw(self.window)
          self.title.draw(self.window)
          self.play.draw(self.window)
          self.tuto.draw(self.window)
          
        
class TutoScene(Scene):
        def __init__(self,window,asset,fps):
          self.player=Entity.Player(640,360,asset["Image"]["ROCKET"])
          self.ROCK=Entity.Rock(0,asset["Image"]["ROCK"])
          self.ROCK.rect.center=(1000,400)
          KEY=asset["Image"]["UI"]["KEY"]
          self.Key_UP=UI.Key((300,150),KEY["KEY0.png"],KEY["KEY1.png"])
          self.Key_DOWN=UI.Key((300,300),KEY["KEY2.png"],KEY["KEY3.png"])
          self.Key_RIGHT=UI.Key((450,300),KEY["KEY4.png"],KEY["KEY5.png"])
          self.Key_LEFT=UI.Key((150,300),KEY["KEY6.png"],KEY["KEY7.png"])
          super().__init__(window,fps)
         
        def process(self,delta):
           
              velocity=pygame.Vector2(0,0)
              keys=pygame.key.get_pressed()
              if keys[pygame.K_UP] or keys[pygame.K_z]:
                    self.Key_UP.value=True
                    velocity.y-=1
              else:
                    self.Key_UP.value=False
              if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    self.Key_DOWN.value=True
                    velocity.y+=1
              else:
                    self.Key_DOWN.value=False
        
              if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.Key_RIGHT.value=True
                    velocity.x+=1
              else:
                    self.Key_RIGHT.value=False

              if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                    self.Key_LEFT.value=True
                    velocity.x-=1
              else:
                   self.Key_LEFT.value=False
              
              self.Key_UP.update(delta)
              self.Key_DOWN.update(delta)
              self.Key_RIGHT.update(delta)
              self.Key_LEFT.update(delta)
              self.player.update(velocity,delta)
              if pygame.sprite.collide_mask(self.ROCK,self.player)!=None:
                  return True
        def render(self):
              self.window.fill((0,225,0))
              self.window.blit(self.player.image,self.player.rect)
              self.window.blit(self.ROCK.image,self.ROCK.rect)
              self.Key_UP.draw(self.window)
              self.Key_DOWN.draw(self.window)
              self.Key_RIGHT.draw(self.window)
              self.Key_LEFT.draw(self.window)
     
class GameOver(Scene):
     def __init__(self,window,asset,score,TextColor,fps):
          SufaceText=asset["Font"]["NumSpace.ttf"].render(f"{score}",True,TextColor)
          self.text=ImageAnimation((650,500),SufaceText,"rotate",(0,360),1)
          self.reset=UI.Button((300,500),asset["Image"]["UI"]["RESET.png"].copy(),(1,1.5),0.5)
          self.home=UI.Button((1000,500),asset["Image"]["UI"]["HOME.png"].copy(),(1,1.5),0.5)
          self.title=ImageAnimation((650,200),asset["Image"]["UI"]["GAMEOVER.png"].copy(),"scale",(0,1),1)
          super().__init__(window,fps)
     def process(self, delta):
           self.home.update(delta)
           self.reset.update(delta)
           self.title.update(delta,True)
           self.text.update(delta,True)
           if(self.reset.is_click()):
                return "RESET"
           if(self.home.is_click()):
                return "MENU"
           
     def render(self):
          self.window.fill((255,255,255))
          self.title.draw(self.window)
          self.reset.draw(self.window)
          self.home.draw(self.window)
          self.text.draw(self.window)
