"""
Copyright 2019, Aleksandar Stojimirovic <stojimirovic@yahoo.com>

Licence: MIT
Source: https://github.com/hooppler/wormnet/
"""

import pygame
from math import *


class DrawingMatrix(object):
    def __init__(self, width=300, height=300, fields_x=20, fields_y=20, pos_x=0, pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.max_diameter = min([self.width, self.height])
        self.fields_x = fields_x
        self.fields_y = fields_y
        self.max_fields = max([self.fields_x, self.fields_y])
        self.d = int(round(float(self.max_diameter)/float(self.max_fields)))
        self.dx = self.width/self.fields_x
        self.dy = self.height/self.fields_y

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_alpha(100)
        
        
        self.fields = []
        for x in range(0, self.fields_x):
            for y in range(0, self.fields_y):
                self.fields.append(0)
                
        #                          R    G    B
        self.BLACK = pygame.Color( 0 ,  0 ,  0 )
        self.WHITE = pygame.Color(255, 255, 255)
        self.COLOR1 = pygame.Color(255,255,180)
        self.COLOR2 = pygame.Color(88,88,88)
                
    
    
    def update(self):
        
        m_x, m_y = pygame.mouse.get_pos()
        m_x = m_x - self.pos_x
        m_y = m_y - self.pos_y
        s_x = int(floor(m_x/self.dx))
        s_y = int(floor(m_y/self.dy))
        
        if (s_x<self.fields_x and s_y<self.fields_y) and (s_x>=0 and s_y>=0):
            self.fields[s_y * self.fields_x + s_x] = 1

        for x in range(0, self.fields_x):
            for y in range(0, self.fields_y):
                if self.fields[y*self.fields_x + x] == 0:
                    pygame.draw.rect(self.surface, self.COLOR1, (x*self.dx, y*self.dy, self.dx, self.dy))
                else:
                    pygame.draw.rect(self.surface, self.COLOR2, (x*self.dx, y*self.dy, self.dx, self.dy))

        for x in range(0, self.fields_x+1):
            pygame.draw.line(self.surface, self.BLACK, (x*self.dx, 0), (x*self.dx, self.fields_y*self.dy))
        for y in range(0, self.fields_y+1):
            pygame.draw.line(self.surface, self.BLACK, (0, y*self.dy), (self.fields_x*self.dx, y*self.dy))
    
    
    def get_surface(self):
        return self.surface
    
    
    def get_pattern(self):
        return self.fields
        
        
    def clear(self):
        for x in range(0, self.fields_x):
            for y in range(0, self.fields_y):
                self.fields[y*self.fields_x+x] = 0
    