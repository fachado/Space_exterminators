class NaveEspacial:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 4
        self.moving_left = False
        self.moving_right = False
        self.vidas = 3
        self.vidas_iniciales = 3
        self.posicion_inicial = (x, y)

    def mueve(self):
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed

    def limitar_bordes(self, screen_width, screen_height):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def restar_vida(self):
        self.vidas -= 1

    def reiniciar_posicion(self):
        self.rect.center = self.posicion_inicial
        self.vidas = self.vidas_iniciales

    def obtener_vidas(self):
        return self.vidas