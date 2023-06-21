import pygame

class ProyectilNave:
    def __init__(self, x, y, image):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.image = image

    def mover(self, velocidad):
        self.rect.y -= velocidad

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)