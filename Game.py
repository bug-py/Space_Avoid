import os
import pickle

import pygame

import Scene

class Game():
   def __init__(self):
     pygame.init()
     self.window=pygame.display.set_mode((1280,720))
     self.asset=self.load("./Asset")
     self.HighScore=self.load_score()
     pygame.display.set_caption("Space Avoid")
     pygame.display.set_icon(self.asset["Image"]["ICON.png"])
     
   def save_score(self):
      with open("Score.dat","wb") as file :
         pickle.dump(self.HighScore,file)
         
   def load_score(self):
      try:
         with open("Score.dat","rb") as file:
            score=pickle.load(file)
         if(type(score)!=int):
            return 0
         return score
      except:
         return 0

   def load(self,root):
     asset={}
     entries=os.scandir(root)
     for entry in entries:
        name=entry.name
        if entry.is_file():
            extension=name.split('.')[-1]
            path=os.path.join(root,name)
            if  extension =="png":
                asset[name]=pygame.image.load(path).convert_alpha()
            if extension=="mp3":
                asset[name]=pygame.mixer.Sound(path)
            if extension=="ttf":
                asset[name]=pygame.font.Font(path,200)
               
        elif entry.is_dir():
            asset[name]=self.load(os.path.join(root,name))
     return asset
   def play(self):
      while(True):
         MainScene=Scene.MainScene(self.window,self.asset,120)
         score=MainScene.start()
         TextColor=(0,0,0)
         if(score>self.HighScore):
            TextColor=(184,134,11)
            self.HighScore=score
            self.save_score() 
         GameOver=Scene.GameOver(self.window,self.asset,score,TextColor,120)
         if(GameOver.start()=="MENU"):
                 break
   def run(self):
      self.asset["Sound"]["Space.mp3"].play(-1)
      while(True):
       MenuScene=Scene.MenuScene(self.window,self.asset,120)
       choice=MenuScene.start()
       if(choice=="TUTO"):
         TutoScene=Scene.TutoScene(self.window,self.asset,120)
         TutoScene.start()
       elif(choice=="PLAY"):     
         self.play()

Game().run()