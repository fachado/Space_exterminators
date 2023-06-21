import pygame
def cargar_imagenes_explosion(tamañoy,tamañox):
    frames_explosion = []
    for i in range(1, 10):
        frame = pygame.image.load(f"PYGAME/frames explosiones/explosion_{i}.png")
        frame = pygame.transform.scale(frame, (tamañoy, tamañox))
        frames_explosion.append(frame)
    return frames_explosion

# Cargar imágenes de explosión previamente

# Clase para la animación de explosión
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,frames_explosion):
        super().__init__()
        self.frames = frames_explosion
        self.current_frame = 0
        self.animation_speed = 100
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.animation_speed:
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.current_frame]
            self.last_update = now
        