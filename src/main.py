"""
Copyright 2019, Aleksandar Stojimirovic <stojimirovic@yahoo.com>

Licence: MIT
Source: https://github.com/hooppler/wormnet/
"""

import pygame
from pygame.locals import *
import sys, os
import time
import string
from textinput import TextInput
from drawing_matrix import DrawingMatrix
from neural_network import NeuralNetwork
from button import Button


class CharacterRecognitionGUI(object):
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Neural Network Letter Recognition')
        
        pygame.font.init()
        self.font1 = pygame.font.SysFont('Comic Sans MS', 20)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 15)
        
        fpsClock = pygame.time.Clock()
        
        self.window = pygame.display.set_mode((800, 600))
        self.canvas = self.window.copy()
        self.mouse = pygame.mouse
        self.colors = Colors()

        self.title = self.font1.render('Can Roundworm Learn Alphabet ?', False, (0,0,0))
        self.cycle_label = self.font2.render('Cycle:', False, (0,0,0))
        self.cycle_text = self.font2.render(' ', False, (0,0,0))
        self.help1_text = self.font2.render('1. Draw by mouse uppercase letter A-Z at the left panel.', False, (0,0,0))
        self.help2_text = self.font2.render('2. Black letter on the right shows current Neural Network output.', False, (0,0,0))
        self.help3_text = self.font2.render('3. Delete current network output (Backspace) and write desired ouput.', False, (0,0,0))
        self.help4_text = self.font2.render('4. Desired output is colored red.', False, (0,0,0))
        self.help5_text = self.font2.render('5. Wait network to learn desired output.', False, (0,0,0))
        self.help6_text = self.font2.render('6. Delete desired output (Backspace) to check what network have been learned.', False, (0,0,0))
        
        self.drawing_matrix = DrawingMatrix(width=300, height=300, fields_x=8, fields_y=8, pos_x=30, pos_y=50)
        self.nn_image = pygame.image.load('../media/NeuralNetwork198x210.png')
        self.roundwarm_image = pygame.image.load('../media/RoundWarmNervousSystem.png')
        self.textinput = TextInput(font_size=200)
        
        self.text_background_surface = pygame.Surface((200, 200))
        pygame.draw.rect(self.text_background_surface, self.colors.COLOR1, (0, 0, 200, 200))

        self.canvas.fill(self.colors.WHITE)
        self.drawing_matrix.update()

        self.button = Button(width=150, height=30, pos_x=100, pos_y=355, title='Clear')
        
        # Neural Network Initialization
        self.nn = NeuralNetwork()
        self.nn.set_random_w()

        self.converter = EncodingConverter()
        
        
    def run(self):
    
        cnt = 0
        cycle = 0
        
        while True:
            left_pressed, middle_pressed, right_pressed = self.mouse.get_pressed()
            events = pygame.event.get()
            
            self.nn.set_input(self.drawing_matrix.get_pattern())
            self.nn.feed_forward()
            output = self.nn.get_output()
            
            for event in events:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif left_pressed:
                    self.drawing_matrix.update()
                elif event.type == KEYDOWN:
                    cnt = 10
                    self.textinput.set_text_color((235,34,3))
            if (cnt <= 0 and self.textinput.get_text()=='') or self.textinput.get_text_color()==(0,0,0):
                self.textinput.clear_text()
                
                letter = self.converter.onehot_to_letter(vec=output)

                self.textinput.set_text(letter)
                self.textinput.set_text_color((0,0,0))
            else:
            
                tp_output = self.converter.letter_to_onehot(letter = self.textinput.get_text())
                if not tp_output is None:
                    t_output = tp_output
                
                self.nn.set_delta_output(t_output)
                self.nn.back_propagation()
                self.nn.adjust_w()
            
            if self.button.get_state() == 1:
                pass
                self.drawing_matrix.clear()
            
            self.textinput.update(events)
            self.button.update(events)
            cnt -= 1
            
            self.cycle_text = self.font2.render('{}'.format(cycle), False, (0,0,0))
            
            self.window.fill(self.colors.WHITE)
            self.window.blit(self.canvas, (0, 0))
            self.canvas.blit(self.drawing_matrix.get_surface(), (30, 50))
            self.canvas.blit(self.nn_image, (350, 50))
            self.canvas.blit(self.roundwarm_image, (350, 250))
            self.window.blit(self.text_background_surface, (550, 100))
            self.window.blit(self.title, (230, 0))
            self.window.blit(self.cycle_label, (30, 30))
            self.window.blit(self.cycle_text, (90, 30))
            self.window.blit(self.help1_text, (30, 450))
            self.window.blit(self.help2_text, (30, 467))
            self.window.blit(self.help3_text, (30, 484))
            self.window.blit(self.help4_text, (30, 501))
            self.window.blit(self.help5_text, (30, 518))
            self.window.blit(self.help6_text, (30, 535))
            
            
            self.window.blit(self.textinput.get_surface(), (600, 130))
            self.window.blit(self.button.get_surface(), (100, 355))

            pygame.display.update()
            cycle += 1
        
        
class EncodingConverter(object):
    def __init__(self):
        self.d = dict(enumerate(string.ascii_uppercase, 1))
        self.inv_d = {v: k for k, v in self.d.items()}

    def onehot_to_letter(self, vec):
        k = vec.index(max(vec)) + 1
        return self.d[k]
        
    def letter_to_onehot(self, letter):
        if not letter in self.inv_d:
            return None
    
        k = self.inv_d[letter]
        
        vec = []
        for i in range(0, 26):
            if k == i+1:
                vec.append(1)
            else:
                vec.append(0)
        return vec

        
class Colors(object):
        #                     R    G    B
        BLACK = pygame.Color( 0 ,  0 ,  0 )
        WHITE = pygame.Color(255, 255, 255)
        COLOR1 = pygame.Color(255,255,180)
        COLOR2 = pygame.Color(88,88,88)
    
        
if __name__ == '__main__':
    cr_gui = CharacterRecognitionGUI()
    cr_gui.run()






