import pygame
import random

class MisilEnemigo:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5
        


    def update(self):
        self.rect.y += self.speed
        

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)