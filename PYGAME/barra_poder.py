import pygame

class BarraPoder:
    def __init__(self, x, y, ancho, alto, poder_maximo):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.poder_maximo = poder_maximo
        self.poder = 0

    def aumentar_poder(self):
        self.poder += 35
        if self.poder > self.poder_maximo:
            self.poder = self.poder_maximo

    def reiniciar_poder(self):
        self.poder = 0

    def dibujar(self, screen,color):
        pygame.draw.rect(screen, color, (self.x, self.y - self.poder, self.ancho, self.poder))