import pygame
from os.path import join 

class growplant:
    def __init__(self,rect, image , mony):
        self.rect = rect
        self.image = image
        self.clock = pygame.time.Clock()
        self.mony= mony
        self.seconds= 10000
        self.start_time = 0          
        self.planted = False
        self.grown = False
        self.ready = False
    def plant(self):
        
        self.planted = True
        self.grown = False
        self.start_time = pygame.time.get_ticks()         
    def collected(self):
        self.planted = False
        self.grown = False
        
    def update (self):
        if self.planted and pygame.time.get_ticks() - self.start_time >= self.seconds:
            self.planted = False
            self.grown = True
    def draw(self,screen,imggrown):
        if self.grown:
            screen.blit(self.image,self.rect)
        elif self.planted:
            screen.blit(imggrown, self.rect)
        
        #  have to add if the 10 seconds are over to display a img and change the grown to false 
            
                
            



