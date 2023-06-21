import pygame
import caracteristicas
class Boss:
    def __init__(self, image, x, y, vida, velocidad):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # Dirección inicial (1: derecha, -1: izquierda)
        self.vida = vida
        self.velocidad = velocidad
        self.velocidad_proyectil = 8
        self.last_shot_time = 0  # Tiempo en milisegundos de la última vez que disparó
        self.shoot_delay = 2000
        self.boss_proyectil = None
        self.visible = True
        self.shoot_sound = pygame.mixer.Sound("PYGAME/sonidos/boss_disparo.mp3")

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.boss_proyectil = BossProyectil(self.rect.x + 55, self.rect.y + 160, self.velocidad_proyectil)
            self.last_shot_time = current_time
            self.shoot_sound.play()
    def restar_vida(self, resta):
        self.vida -= resta

    def update(self):
        # Mover el Boss de izquierda a derecha
        self.rect.x += self.direction * self.velocidad

        # Verificar los bordes de la pantalla
        if self.rect.right >= caracteristicas.width or self.rect.left <= 0:
            self.direction *= -1  # Cambiar de dirección

        if self.boss_proyectil is not None:
            self.boss_proyectil.update()
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)
        if self.boss_proyectil is not None:
            self.boss_proyectil.draw(screen)

class BossProyectil:
    def __init__(self, x, y, velocidad):
        self.image = pygame.image.load("PYGAME/proyectil_boss.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.y += self.velocidad

    def draw(self, screen):
        screen.blit(self.image, self.rect)

