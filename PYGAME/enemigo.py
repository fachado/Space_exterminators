import pygame

espacio_entre_enemigos = 150

posicion_y = 80
tiempo_inicio = pygame.time.get_ticks()
tiempo_actual = pygame.time.get_ticks()
tiempo_transcurrido = (tiempo_actual - tiempo_inicio) / 1000
class Enemigo:
    def __init__(self, x, y, imagen,velocidad):
        self._image = imagen
        self._rect = self._image.get_rect()
        self._rect.x = x
        self._rect.y = y
        self.velocidad = velocidad # Velocidad de movimiento del enemigo
        self.ultimo_lanzamiento = 0 
    def mover(self):
        self._rect.x += self.velocidad

    def dibujar(self, screen):
        screen.blit(self._image, self._rect)

    def cambiar_lado(self, pantalla_ancho):
        if self._rect.right >= pantalla_ancho or self._rect.left <= 0:
            self.velocidad *= -1

    def eliminar(self, enemigos):
        if self in enemigos:
            enemigos.remove(self)

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

 


            
    @staticmethod
    def crear_enemigos(enemigo_image,cantidad_enemigos,velocidad):
        enemigos = []
        fila_actual = 0  # Variable para controlar la fila actual de enemigos
        
        for i in range(cantidad_enemigos):
            posicion_x = espacio_entre_enemigos * (i % 10 + 1)
            posicion_y_actual = posicion_y + (fila_actual * 90)
            enemigo = Enemigo(posicion_x, posicion_y_actual, enemigo_image,velocidad)
            enemigos.append(enemigo)
            
            if (i + 1) % 10 == 0:
                fila_actual += 1
        
        return enemigos
    
    @staticmethod
    def mover_enemigos(enemigos, direccion, width, screen, tiempo_actual, tiempo_transcurrido):
        enemigos_vivos = []

        for enemigo in enemigos:
            enemigo.rect.x += direccion * enemigo.velocidad

            enemigo.mover()
            enemigo.cambiar_lado(width)
            enemigo.dibujar(screen)

            enemigos_vivos.append(enemigo)

        primer_enemigo = min(enemigos_vivos, key=lambda enemigo: enemigo.rect.left, default=None)
        ultimo_enemigo = max(enemigos_vivos, key=lambda enemigo: enemigo.rect.right, default=None)

        if primer_enemigo is not None and ultimo_enemigo is not None:
            if primer_enemigo.rect.left <= 0 or ultimo_enemigo.rect.right >= width:
                direccion *= -1

        for enemigo in enemigos:
            enemigo.velocidad = direccion * enemigo.velocidad

        return direccion
    def mover_linea(enemigos,velocidad):
        for enemigo in enemigos:
            enemigo.rect.y += velocidad


