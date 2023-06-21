import pygame

def cargar_sonidos():
    pygame.mixer.music.load("PYGAME/sonidos/musica.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    disparo = pygame.mixer.Sound("PYGAME/sonidos/disparos_.mp3")
    gameover = pygame.mixer.Sound("PYGAME/sonidos/game-over-arcade-6435.mp3")
    levelup = pygame.mixer.Sound("PYGAME/sonidos/level up.mp3")
    disparo_power = pygame.mixer.Sound("PYGAME/sonidos/disparo_power.wav")
    dead = pygame.mixer.Sound("PYGAME/sonidos/muerte.wav")
    dead.set_volume(0.2)
    
    return disparo, gameover, levelup, disparo_power, dead
def cargar_imagen(ruta, dimensiones):
    imagen = pygame.image.load(ruta)
    imagen = pygame.transform.scale(imagen, dimensiones)
    return imagen