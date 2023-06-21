import pygame


import colores

pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")
background_image = pygame.image.load("PYGAME/menu.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
def pantalla_previa(nivel,juego):
    pygame.init()

    screen_width, screen_height = 1920, 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pantalla Previa")
    
    font = pygame.font.Font("PYGAME\ANTQUABI.TTF", 46)
    texto = font.render(f" - Nivel {nivel} - Juego en 3 segundos", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.blit(texto, texto_rect)
    pygame.display.flip()
    
    pygame.time.delay(3000)  # Pausa de 3 segundos
    
    pygame.quit()
    juego()  # Iniciar el juego después de la pausa


def mostrar_menu(nivel,juego):
    menu_font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", 35)
    pygame.mixer.music.load("PYGAME\sonidos\musica_menu.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    text_size=170
    game_over_font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", text_size)
    game_over_text = game_over_font.render("Space Exterminators", True, colores.VIOLETA)
    opciones = [" Jugar ", " Instrucciones ", " Salir "]
    selected_option = 0
    opcion_image = pygame.image.load("PYGAME/asset_opcion.png")
    opcion_image = pygame.transform.scale(opcion_image, (500,200))
    while True:
        screen.blit(background_image, (0, 0))
        
        screen.blit(opcion_image, (710, 440))
        screen.blit(opcion_image, (710, 560))
        screen.blit(opcion_image, (710, 680))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(opciones)
                    while opciones[selected_option] == "":
                        selected_option = (selected_option - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(opciones)
                    while opciones[selected_option] == "":
                        selected_option = (selected_option + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                        # Acción dependiendo de la opción seleccionada
                        if selected_option == 0:
                            pygame.mixer.music.stop()
                            pantalla_previa(nivel,juego)
                            pygame.quit()  # Función para comenzar el juego
                        if selected_option == 2:
                            pygame.quit()
                        if selected_option==1:
                            mostrar_instrucciones(nivel,juego)

        for i, opcion in enumerate(opciones):
            if opcion != "":
                text = menu_font.render(opcion, True, (255, 255, 255) if i != selected_option else colores.VIOLETA)
                text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2 + i * 118))
                screen.blit(text, text_rect)
        screen.blit(game_over_text, (100,200))
        
        pygame.display.flip()

def mostrar_instrucciones(nivel,juego):
    pygame.init()

    # Configuración de la ventana del juego

    ventana = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Instrucciones del juego")

    # Configuración de la fuente y el texto
    fuente = pygame.font.SysFont("PYGAME\ARCADECLASSIC.TTF", 36)
    texto = '''Instrucciones del juego

    1 muevete usando las flechas de dirección

    2 Dispara con la tecla de Q Y E

    3 carga power-ups para disparar un misil cargado con la x

    4 Obtén la mayor puntuación posible

    Diviértete jugando
    '''

    # Separar las líneas de texto
    lineas = texto.split('\n')

    # Configuración del botón de volver
    boton_volver = pygame.Rect(800, 700, 100, 50)
    color_boton = (255, 0, 0)

    # Ciclo principal del juego
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1 and boton_volver.collidepoint(evento.pos):
                    mostrar_menu(nivel,juego)
                    ejecutando = False

        # Dibujar el fondo, el texto y el botón en la ventana
        ventana.fill((0, 0, 0))
        y = 300  # Posición vertical inicial del texto
        for linea in lineas:
            superficie_texto = fuente.render(linea, True, (255, 255, 255))
            ventana.blit(superficie_texto, (300, y))
            y += 30  # Aumentar la posición vertical para la siguiente línea

        pygame.draw.rect(ventana, color_boton, boton_volver)
        texto_volver = fuente.render("Volver", True, (0, 0, 0))
        texto_rect = texto_volver.get_rect(center=boton_volver.center)
        ventana.blit(texto_volver, texto_rect)

        pygame.display.flip()

    pygame.quit()

# Llamada a la función mostrar_instrucciones
