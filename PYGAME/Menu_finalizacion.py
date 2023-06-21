import pygame
import sqlite3
import random
import pygame
import sqlite3
import personaje
# Constantes
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


# Función para crear estrellas aleatorias
def crear_estrellas():
    STAR_COUNT = 70
    
    estrellas = []
    for _ in range(STAR_COUNT):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        estrellas.append((x, y))
    return estrellas

# Función para mover las estrellas hacia abajo
def mover_estrellas(estrellas):
    STAR_SPEED = 2
    nuevas_estrellas = []
    for x, y in estrellas:
        nueva_y = y + STAR_SPEED
        if nueva_y > SCREEN_HEIGHT:
            nueva_y = 0
            x = random.randint(0, SCREEN_WIDTH)
        nuevas_estrellas.append((x, nueva_y))
    return nuevas_estrellas

# Función para mostrar el menú de finalización
def crear_naves_espaciales(nave_espacial_image):
    naves_espaciales = []
    nave_espacial = personaje.NaveEspacial(SCREEN_WIDTH // 2, SCREEN_HEIGHT, nave_espacial_image)
    naves_espaciales.append(nave_espacial)
    return naves_espaciales

# Función para dibujar naves espaciales
def dibujar_naves_espaciales(naves_espaciales, screen):
    for nave_espacial in naves_espaciales:
        screen.blit(nave_espacial.image, nave_espacial.rect)

# Función para actualizar las naves espaciales
def actualizar_naves_espaciales(naves_espaciales):
    for nave_espacial in naves_espaciales:
        nave_espacial.rect.y -= nave_espacial.speed
        if nave_espacial.rect.bottom < 0:
            naves_espaciales.remove(nave_espacial)

# Resto del código...

def mostrar_menu_finalizacion(puntuacion):
    pygame.init()
    pygame.mixer.music.load("PYGAME\sonidos\musica_gameover.mp3")
    pygame.mixer.music.play(-1)
    nave_espacial_image = pygame.image.load("PYGAME/nave.png")
    nave_espacial_image = pygame.transform.scale(nave_espacial_image, (70, 70))
    naves_espaciales = crear_naves_espaciales(nave_espacial_image)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", 36)
    input_box = pygame.Rect(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    background_image = pygame.image.load("PYGAME/fondofin.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    nombre = ''
    input_text = ''
    estrellas = crear_estrellas()  # Crear las estrellas

    # Variables para el texto "Game Over"
    text_size = 200
    text_position = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    text_visible = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        nombre = input_text
                        guardar_puntuacion(nombre, puntuacion)
                        mostrar_puntuaciones(screen)
                        pygame.mixer.music.stop
                        pygame.display.flip()
                        pygame.time.wait(3000)
                        pygame.quit()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Verificar límite máximo de caracteres
                        if len(input_text) < 10:
                            input_text += event.unicode
        screen.blit(background_image,(0,0))
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(input_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))
        mostrar_puntaje(screen, puntuacion)
        # Dibujar las estrellas
        for x, y in estrellas:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)

        # Dibujar el texto "Game Over" si es visible
        game_over_font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", text_size)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=text_position)
        screen.blit(game_over_text, text_rect)

        # Dibujar las naves espaciales
        dibujar_naves_espaciales(naves_espaciales, screen)
        font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", 36)
        text_surface = font.render(f"Insert your name", True, (255, 255, 255))
        screen.blit(text_surface, (820, 430))
        pygame.display.flip()
        clock.tick(30)

        # Actualizar las estrellas
        estrellas = mover_estrellas(estrellas)
        # Actualizar el tamaño y la posición del texto "Game Over" si es visible
        if text_visible:
            if text_size > 0:
                text_size -= 1
            if text_position.y > 0:
                text_position.y -= 10
            if text_size == 178:
                text_position.y = text_position.y
                text_visible = False

        # Actualizar las naves espaciales
        actualizar_naves_espaciales(naves_espaciales)
        if len(naves_espaciales) < 5:
            nueva_nave_espacial = personaje.NaveEspacial(
                random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, nave_espacial_image
            )
            naves_espaciales.append(nueva_nave_espacial)
pygame.quit


# Función para crear la tabla puntuaciones si no existe
def crear_tabla_puntuaciones():
    conexion = sqlite3.connect("puntuaciones.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS puntuaciones
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    puntuacion INTEGER NOT NULL)''')
    conexion.commit()
    conexion.close()

# Función para guardar la puntuación en la base de datos
def guardar_puntuacion(nombre, puntuacion):
    conexion = sqlite3.connect("puntuaciones.db")
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO puntuaciones (nombre, puntuacion) VALUES (?, ?)", (nombre, puntuacion))
    conexion.commit()
    conexion.close()

# Función para mostrar las puntuaciones
def mostrar_puntuaciones(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 36)
    text_surface = font.render("--- Puntuaciones ---", True, (0, 0, 0))
    screen.blit(text_surface, (300, 100))

    conexion = sqlite3.connect("puntuaciones.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, puntuacion FROM puntuaciones ORDER BY puntuacion DESC LIMIT 5")
    puntuaciones = cursor.fetchall()

    y = 200
    for i, (nombre, puntuacion) in enumerate(puntuaciones):
        text_surface = font.render(f"{i+1}. {nombre}: {puntuacion}", True, (0, 0, 0))
        screen.blit(text_surface, (300, y))
        y += 50

    conexion.close()
def mostrar_puntaje(screen, puntaje):
    font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", 36)
    text_surface = font.render(f"Highscore {puntaje}", True, (255, 255, 255))
    screen.blit(text_surface, (850, 630))


# Función para mover las estrellas hacia abajo

# Crear la tabla de puntuaciones si no existe
crear_tabla_puntuaciones()

# Ejemplo de uso
 # Aquí deberías usar la puntuación real obtenida en el juego

