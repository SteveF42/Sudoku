import pygame
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
GREY = (150,150,150,0)
ORANGE = (255,255,0)

class Node:
    def __init__(self,row,col,width,value = 0):
        pygame.font.init()
        self.value = value
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.width = width
        self.color = WHITE
        self.locked = False
    def lock(self):
        self.locked = True

    def get_pos(self):
        return (self.row,self.col)

    def set_value(self, value):
        self.value = value
        
    def get_value(self):
        return self.value    
    
    def get_pos(self):
        return (self.row,self.col)
    
    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.width))
        if self.value != 0:
            font = pygame.font.SysFont('comicsans',38)
            message = font.render(str(self.value),True,BLACK)
            window.blit(message,(self.x + self.width//2.3,self.y + self.width//3))

    def make_solved(self):
        self.color = GREEN

    def make_solving(self):
        self.color = RED

    def make_open(self):
        self.color = WHITE
    
    def make_selected(self):
        self.color = GREY
    
    def make_orange(self):
        self.color = ORANGE


    

