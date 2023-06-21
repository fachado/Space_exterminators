import pygame


def mostrar_temporizador(screen, duracion_temporizador, x, y, fuente, color,tiempo_inicial):
    tiempo_transcurrido = (pygame.time.get_ticks() - tiempo_inicial) // 1000
    minutos = tiempo_transcurrido // 60
    segundos = tiempo_transcurrido % 60
    tiempo_restante = max(duracion_temporizador - tiempo_transcurrido, 0)
    texto_temporizador = fuente.render("{:02d}:{:02d}".format(minutos, segundos), True, color)
    screen.blit(texto_temporizador, (x, y))
    return tiempo_restante
        
                    
def vidas_pantalla(personaje,imagen,screen):
    if personaje.obtener_vidas()==3:
        screen.blit(imagen, (1800,0))
        screen.blit(imagen, (1750,0))
        screen.blit(imagen, (1700,0))
    elif personaje.obtener_vidas()==2:
        screen.blit(imagen, (1800,0))
        screen.blit(imagen, (1750,0))
    else:
        screen.blit(imagen, (1800,0))

def barra_poder_cargada(barra):
        proyectil_cargado=False
        if barra.poder >= barra.poder_maximo:
            proyectil_cargado = True

        return proyectil_cargado
def actualizar_misiles_enemigos(lista_misiles,screen):
    for misil in lista_misiles:
        misil.update()
        misil.dibujar(screen)

def mostrar_texto(screen, texto, posicion, color):
    fuente = pygame.font.Font(None, 30)
    texto_renderizado = fuente.render(texto, True, color)
    screen.blit(texto_renderizado, posicion)
def actualizar_pnormal(lista_pn,screen):
    for proyectil in lista_pn:
            proyectil.mover(3)  # Velocidad de los proyectiles lanzados
            proyectil.dibujar(screen)
def actualizar_ppower(lista_pw,screen):
    for proyectil in lista_pw:
            proyectil.mover(6)  # Velocidad de los proyectiles lanzados
            proyectil.dibujar(screen)
def dibujar_estrellas(lista_estrellas,screen):
    for x, y in lista_estrellas:
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)