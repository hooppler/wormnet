"""
Copyright 2019, Aleksandar Stojimirovic <stojimirovic@yahoo.com>

Licence: MIT
Source: https://github.com/hooppler/wormnet/
"""

import pygame


class Button(object):
    def __init__(self, width=60, height=20, pos_x=0, pos_y=0, title='Button'):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.title = title
        self.font_size = 20
        self.state = 0
        
        self.surface = pygame.Surface((width, height))
        
        # Text Initialization
        pygame.font.init()
        font = pygame.font.SysFont('Arial', self.font_size)
        self.text_surface = font.render(title, False, (0,0,0))
        
        
    def update(self, events):
    
        left_pressed, midle_pressed, right_pressed = pygame.mouse.get_pressed()
        self.state = 0
        for event in events:
            if left_pressed:
                pos_x, pos_y = pygame.mouse.get_pos()
                pos_x = pos_x - self.pos_x
                pos_y = pos_y - self.pos_y
                if (pos_x > 0 and pos_x < self.width) and (pos_y > 0 and pos_y < self.height):
                    self.state = 1
                    pygame.draw.rect(self.surface, pygame.Color(130,130,74), (0, 0, self.width, self.height))
                else:
                    pygame.draw.rect(self.surface, pygame.Color(195,192,105), (0, 0, self.width, self.height))
            else:
                pygame.draw.rect(self.surface, pygame.Color(195,192,105), (0, 0, self.width, self.height))

        self.surface.blit(self.text_surface, ((self.width-(self.font_size/2)*len(self.title))/2, (self.height-self.font_size)/2-2))
    
    
    def get_surface(self):
        return self.surface
        
        
    def get_state(self):
        return self.state
        
