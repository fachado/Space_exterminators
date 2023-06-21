import pygame
from barra_poder import BarraPoder
import personaje
import proyectil_personaje
import colores
import colisiones
import caracteristicas
from puntos import Puntaje
from enemigo import Enemigo
import Misiles_enemigos
import random
import Menu_finalizacion
from explosiones import Explosion
import explosiones
import funciones_juego
import funciones_de_carga
import menu
from boss import Boss

puntuaciones = {}
def disparar_enemigos_aleatorios(enemigos, imagen_misil, misiles_enemigos):
    
    enemigos_aleatorios = random.sample(enemigos, 1)
    disparo = pygame.mixer.Sound("PYGAME\sonidos\enemigo.mp3")
    
    for enemigo in enemigos_aleatorios:
        misil_enemigo = Misiles_enemigos.MisilEnemigo(enemigo.rect.centerx, enemigo.rect.bottom, imagen_misil)
        disparo.play()
        misiles_enemigos.append(misil_enemigo)

def jugar():
    nivel = 1
    
    pygame.init()

    disparo, gameover, levelup, disparo_power, dead = funciones_de_carga.cargar_sonidos()

    screen = pygame.display.set_mode((caracteristicas.width, caracteristicas.height))
    pygame.display.set_caption("Mi Juego")
    #control puntaje
    puntaje = Puntaje()
    #MARCO DE PUNTAJE

    #carga de imagenes
    scoreboard = funciones_de_carga.cargar_imagen("PYGAME/SCORE_VERDE.png", (300, 95))
    nave_espacial_image = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (100, 100))
    nave_espacial_image_vidas = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (50, 50))
    proyectil_normal_image = funciones_de_carga.cargar_imagen("PYGAME/Bala_pj.png", (20, 45))
    misil_power_image = funciones_de_carga.cargar_imagen("PYGAME/bala_power.png", (50, 80))
    enemigo_image = funciones_de_carga.cargar_imagen("PYGAME/enemigo_1.png", (70, 51))
    misil_enemigo_image = funciones_de_carga.cargar_imagen("PYGAME/bala_enemigo_1.png", (30, 55)) 


    # Configura la duración del temporizador en segundos
    duracion_temporizador = 300

    # Obtiene el tiempo inicial del temporizador
    tiempo_inicial = pygame.time.get_ticks()
    fuente = pygame.font.SysFont("Arial", 46)


    nave_espacial = personaje.NaveEspacial(caracteristicas.width // 2, caracteristicas.height, nave_espacial_image)
    running = True

    proyectiles_lanzados = []  # Lista para almacenar los proyectiles lanzados
    tiempo_recarga = 0.8  
    ultimo_lanzamiento = 0  
    proyectiles_lanzados_power=[]

    proyectil_cargado = False

    

    barra = BarraPoder(20, 700, 20, 200, 350)
    # Bucle principal del juego

    direccion_enemigos=1
    enemigos = Enemigo.crear_enemigos(enemigo_image,20,0.6)
    misiles_enemigos_lanzados=[]
    tiempo_recarga_e = 1 

    explosion = pygame.sprite.Group()

    estrellas=Menu_finalizacion.crear_estrellas()
    #manejo de tiempos
    clock = pygame.time.Clock()
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_ultimo_movimiento = tiempo_inicio
    ultimo_disparo_enemigos = pygame.time.get_ticks()

    #fuentes y textos
    puntaje_font = pygame.font.Font(None, 36)
    tope_font=pygame.font.Font(None,36)
    tope_texto = tope_font.render("Full Power", True, colores.ROJO)
    

    while running:
        dt = clock.tick() 
        proyectil_e = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx + 40, nave_espacial.rect.y - 18, proyectil_normal_image)
        proyectil_q= proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx - 50, nave_espacial.rect.y - 18, proyectil_normal_image)
        for event in pygame.event.get():
            #navemovimiento
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = True

                #proyectiles    
                if event.key == pygame.K_e:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()
                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_e)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                elif event.key == pygame.K_q:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()

                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_q)
                        ultimo_lanzamiento = pygame.time.get_ticks()

                elif event.key == pygame.K_x:
                    if proyectil_cargado:
                        disparo_power.play()
                        proyectil = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx-31 , nave_espacial.rect.y-36 , misil_power_image)
                        proyectiles_lanzados_power.append(proyectil)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                        
                        proyectil_cargado = False
                        barra.reiniciar_poder()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = False
      
    # Continuar el juego normalmente
        # Bucle para aplicar cambios y mostrar.
        #movimientos de nave y enemigos
        nave_espacial.mueve()
        nave_espacial.limitar_bordes(caracteristicas.width, caracteristicas.height)
        #mover enemigos hacia abajo cada 2 segundos.
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_ultimo_movimiento) / 1000
        #fondos e imagenes
        screen.fill((0,0, 0))
        screen.blit(nave_espacial.image, nave_espacial.rect)      
        funciones_juego.dibujar_estrellas(estrellas,screen)
        estrellas=Menu_finalizacion.mover_estrellas(estrellas)  
        #mover enemigos
        direccion_enemigos = Enemigo.mover_enemigos(enemigos, direccion_enemigos,  caracteristicas.width, screen,tiempo_actual,tiempo_transcurrido)
        tiempo_actual=0
        #mover balas y dibujar balas
        funciones_juego.actualizar_pnormal(proyectiles_lanzados,screen)
        funciones_juego.actualizar_ppower(proyectiles_lanzados_power,screen)
        #borras al salir del borde

        proyectiles_lanzados = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados))
        proyectiles_lanzados_power = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados_power))
        #textos

        valor_actual = puntaje.obtener()
        puntaje_texto = puntaje_font.render("Score: " + str(valor_actual), True, colores.BLANCO)
        

        screen.blit(scoreboard, (10, 10))
        screen.blit(puntaje_texto, (115, 43))
        screen.blit(tope_texto, (20, 300))
        
        #colisiones + funciones de colisiones

        explosion.update()
        explosion.draw(screen)
        colision=colisiones.detectar_colisiones(proyectiles_lanzados, enemigos,barra,puntaje,explosion)
        colisionpower=colisiones.detectar_colisiones_power(proyectiles_lanzados_power, enemigos,explosion,puntaje)
        colision_enemiga=colisiones.detectar_colisiones_enemigas(misiles_enemigos_lanzados,nave_espacial,explosion,puntaje)

        if colision or colisionpower or colision_enemiga:
            dead.play()

        # Actualiza las animaciones de explosiones
        # Dibuja las explosiones en la pantalla 
        #actualizacion de barra de poder

        barra.dibujar(screen,colores.ROJO)
        proyectil_cargado=funciones_juego.barra_poder_cargada(barra)
        
        #disparos de enemigos con recarga de tiempo

        funciones_juego.actualizar_misiles_enemigos(misiles_enemigos_lanzados,screen)
        if pygame.time.get_ticks() - ultimo_disparo_enemigos > tiempo_recarga_e * 1000:
            disparar_enemigos_aleatorios(enemigos, misil_enemigo_image, misiles_enemigos_lanzados)
            ultimo_disparo_enemigos = pygame.time.get_ticks()

        #desaparecer misilesenemigos si sobrepasan la pantlla

        misiles_enemigos_lanzados = list(filter(lambda misil: misil.rect.bottom < caracteristicas.height, misiles_enemigos_lanzados))
        #mostrar cambios
        #dibujar o sacar vidas
        funciones_juego.vidas_pantalla(nave_espacial,nave_espacial_image_vidas,screen)
        tiempo_restante = funciones_juego.mostrar_temporizador(screen, duracion_temporizador, caracteristicas.width // 2, 0, fuente, colores.BLANCO,tiempo_inicial)
        perdio=Enemigo.perder(enemigos,caracteristicas.height,nave_espacial)

        if len(enemigos) == 0:
            levelup.play()
            bonus_puntos=150
            puntuaciones["nivel_1"] = valor_actual+bonus_puntos+tiempo_restante
            nivel += 1
            cargar_nivel(nivel)

        pygame.display.flip()

        if nave_espacial.obtener_vidas()==0 or perdio:
            pygame.mixer.music.stop()
            gameover.play()
            mostrar_menu_reinicio(valor_actual)
    pygame.quit()


def jugar2():
    nivel = 2

    pygame.init()

    disparo, gameover, levelup, disparo_power, dead = funciones_de_carga.cargar_sonidos()

    screen = pygame.display.set_mode((caracteristicas.width, caracteristicas.height))
    pygame.display.set_caption("Mi Juego")
    #control puntaje
    puntaje = Puntaje()
    #MARCO DE PUNTAJE

    #carga de imagenes
    scoreboard = funciones_de_carga.cargar_imagen("PYGAME/SCORE_VIOLETA.png", (300, 95))
    nave_espacial_image = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (100, 100))
    nave_espacial_image_vidas = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (50, 50))
    proyectil_normal_image = funciones_de_carga.cargar_imagen("PYGAME/Bala_pj.png", (20, 45))
    misil_power_image = funciones_de_carga.cargar_imagen("PYGAME/bala_power.png", (50, 80))
    enemigo_image = funciones_de_carga.cargar_imagen("PYGAME/Alienship.png", (70, 51))
    misil_enemigo_image = funciones_de_carga.cargar_imagen("PYGAME/bala_enemigo_2.png", (20, 45)) 

    duracion_temporizador = 300

    # Obtiene el tiempo inicial del temporizador
    tiempo_inicial = pygame.time.get_ticks()
    fuente = pygame.font.SysFont("Arial", 46)

    #objeto personaje
    nave_espacial = personaje.NaveEspacial(caracteristicas.width // 2, caracteristicas.height, nave_espacial_image)
    running = True
    #listas y proyectiles
    proyectiles_lanzados = []  # Lista para almacenar los proyectiles lanzados
    tiempo_recarga = 0.8  
    ultimo_lanzamiento = 0  
    proyectiles_lanzados_power=[]
    proyectil_cargado = False

    
    #objeto barra
    barra = BarraPoder(20, 700, 20, 200, 350)
    # Bucle principal del juego

    direccion_enemigos=1
    enemigos = Enemigo.crear_enemigos(enemigo_image,30,1)
    misiles_enemigos_lanzados=[]
    tiempo_recarga_e = 0.5

    #animacion explode
    explosion = pygame.sprite.Group()
    #animacion estrellas
    estrellas=Menu_finalizacion.crear_estrellas()
    #manejo de tiempos
    clock = pygame.time.Clock()
    tiempo_inicio = pygame.time.get_ticks()
    tiempo_ultimo_movimiento = tiempo_inicio
    ultimo_disparo_enemigos = pygame.time.get_ticks()

    #fuentes y textos
    puntaje_font = pygame.font.Font(None, 36)
    tope_font=pygame.font.Font(None,36)
    tope_texto = tope_font.render("Full Power", True, colores.AZUL)


    while running:
        dt = clock.tick() 
        proyectil_e = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx + 40, nave_espacial.rect.y - 18, proyectil_normal_image)
        proyectil_q= proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx - 50, nave_espacial.rect.y - 18, proyectil_normal_image)
        for event in pygame.event.get():
            #navemovimiento
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = True

                #proyectiles    
                if event.key == pygame.K_e:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()
                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_e)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                elif event.key == pygame.K_q:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()

                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_q)
                        ultimo_lanzamiento = pygame.time.get_ticks()

                elif event.key == pygame.K_x:
                    if proyectil_cargado:
                        disparo_power.play()
                        proyectil = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx-31 , nave_espacial.rect.y-36 , misil_power_image)
                        proyectiles_lanzados_power.append(proyectil)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                        
                        proyectil_cargado = False
                        barra.reiniciar_poder()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = False
      
    # Continuar el juego normalmente
        # Bucle para aplicar cambios y mostrar.
        #movimientos de nave y enemigos
        nave_espacial.mueve()
        nave_espacial.limitar_bordes(caracteristicas.width, caracteristicas.height)
        #mover enemigos hacia abajo cada 2 segundos.
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_ultimo_movimiento) / 1000
        if tiempo_transcurrido >= 0.1:
            Enemigo.mover_linea(enemigos,1.4)
            tiempo_ultimo_movimiento = tiempo_actual
        #fondos e imagenes
        screen.fill((0,0, 0))
        screen.blit(nave_espacial.image, nave_espacial.rect)      
        funciones_juego.dibujar_estrellas(estrellas,screen)
        estrellas=Menu_finalizacion.mover_estrellas(estrellas)  
        #mover enemigos
        direccion_enemigos = Enemigo.mover_enemigos(enemigos, direccion_enemigos,  caracteristicas.width, screen,tiempo_actual,tiempo_transcurrido)
        tiempo_actual=0
        #mover balas y dibujar balas
        funciones_juego.actualizar_pnormal(proyectiles_lanzados,screen)
        funciones_juego.actualizar_ppower(proyectiles_lanzados_power,screen)
        #borras al salir del borde

        proyectiles_lanzados = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados))
        proyectiles_lanzados_power = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados_power))
        #textos

        valor_actual = puntaje.obtener()
        puntaje_texto = puntaje_font.render("Score: " + str(valor_actual), True, colores.AZUL)
        screen.blit(scoreboard, (10, 10))
        screen.blit(puntaje_texto, (115, 43))
        screen.blit(tope_texto, (20, 300))
        
        #colisiones + funciones de colisiones

        explosion.update()
        explosion.draw(screen)
                            
        colisiones_enemigas=colisiones.detectar_colisiones_enemigas(misiles_enemigos_lanzados,nave_espacial,explosion,puntaje)
        colision=colisiones.detectar_colisiones(proyectiles_lanzados, enemigos,barra,puntaje,explosion)
        colisionpower=colisiones.detectar_colisiones_power(proyectiles_lanzados_power, enemigos,explosion,puntaje)

        if colision or colisionpower or colisiones_enemigas:
            dead.play()

        # Actualiza las animaciones de explosiones
        # Dibuja las explosiones en la pantalla 
        #actualizacion de barra de poder

        barra.dibujar(screen,colores.AZUL)
        proyectil_cargado=funciones_juego.barra_poder_cargada(barra)
        
        #disparos de enemigos con recarga de tiempo

        funciones_juego.actualizar_misiles_enemigos(misiles_enemigos_lanzados,screen)
        if pygame.time.get_ticks() - ultimo_disparo_enemigos > tiempo_recarga_e * 1000:
            disparar_enemigos_aleatorios(enemigos, misil_enemigo_image, misiles_enemigos_lanzados)
            ultimo_disparo_enemigos = pygame.time.get_ticks()

        #desaparecer misilesenemigos si sobrepasan la pantlla

        misiles_enemigos_lanzados = list(filter(lambda misil: misil.rect.bottom < caracteristicas.height, misiles_enemigos_lanzados))
        #mostrar cambios
        #dibujar o sacar vidas
        funciones_juego.vidas_pantalla(nave_espacial,nave_espacial_image_vidas,screen)
        tiempo_restante = funciones_juego.mostrar_temporizador(screen, duracion_temporizador, caracteristicas.width // 2, 0, fuente, colores.AZUL,tiempo_inicial)
        perdio=Enemigo.perder(enemigos,caracteristicas.height,nave_espacial)

        puntuacion_total = sum(puntuaciones.values())
        if len(enemigos) == 0:
            levelup.play()
            bonus_puntos=200
            puntuaciones["nivel_2"] = valor_actual+bonus_puntos+tiempo_restante
            nivel += 1
            cargar_nivel(nivel)
        pygame.display.flip()
        if nave_espacial.obtener_vidas()==0 or perdio:
            pygame.mixer.music.stop()
            gameover.play()
            mostrar_menu_reinicio(puntuacion_total)
    pygame.quit()

def jugar3():
    nivel = 3
    pygame.init()
    disparo, gameover, levelup, disparo_power, dead = funciones_de_carga.cargar_sonidos()
    screen = pygame.display.set_mode((caracteristicas.width, caracteristicas.height))
    pygame.display.set_caption("Mi Juego")
    #control puntaje
    puntaje = Puntaje()
    #MARCO DE PUNTAJE
    vida_boss=20
    velocidad_boss=4.8
    #carga de imagenes
    scoreboard = funciones_de_carga.cargar_imagen("PYGAME/SCORE_NARANJA.png", (300, 95))
    nave_espacial_image = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (100, 100))
    nave_espacial_image_vidas = funciones_de_carga.cargar_imagen("PYGAME/nave.png", (50, 50))
    proyectil_normal_image = funciones_de_carga.cargar_imagen("PYGAME/Bala_pj.png", (20, 45))
    misil_power_image = funciones_de_carga.cargar_imagen("PYGAME/bala_power.png", (50, 80))

    imagen_boss = pygame.image.load("PYGAME/boss.png")
    imagen_boss = pygame.transform.scale(imagen_boss, (180, 180))

    # Crear una instancia del Boss con el tamaño ajustado
    boss = Boss( imagen_boss,100, 100, vida_boss, velocidad_boss)

    duracion_temporizador = 300

    # Obtiene el tiempo inicial del temporizador
    tiempo_inicial = pygame.time.get_ticks()
    fuente = pygame.font.SysFont("Arial", 46)

    #objeto personaje
    nave_espacial = personaje.NaveEspacial(caracteristicas.width // 2, caracteristicas.height, nave_espacial_image)
    running = True
    #listas y proyectiles
    proyectiles_lanzados = []  # Lista para almacenar los proyectiles lanzados
    tiempo_recarga = 0.8  
    ultimo_lanzamiento = 0  
    proyectiles_lanzados_power=[]
    proyectil_cargado = False

    #objeto barra
    barra = BarraPoder(20, 700, 20, 200, 350)
    # Bucle principal del juego

    #animacion explode
    explosion = pygame.sprite.Group()
    #animacion estrellas
    estrellas=Menu_finalizacion.crear_estrellas()
    #manejo de tiempos
    clock = pygame.time.Clock()
  
    #fuentes y textos
    puntaje_font = pygame.font.Font(None, 36)
    tope_font=pygame.font.Font(None,36)
    tope_texto = tope_font.render("Full Power", True, colores.NARANJA)

    while running:
        dt = clock.tick() 
        proyectil_e = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx + 40, nave_espacial.rect.y - 18, proyectil_normal_image)
        proyectil_q= proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx - 50, nave_espacial.rect.y - 18, proyectil_normal_image)
        for event in pygame.event.get():
            #navemovimiento
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = True
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = True

                #proyectiles    
                if event.key == pygame.K_e:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()
                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_e)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                elif event.key == pygame.K_q:
                    if pygame.time.get_ticks() - ultimo_lanzamiento > tiempo_recarga * 1000:
                        disparo.play()

                        # Lanzar proyectil
                        
                        proyectiles_lanzados.append(proyectil_q)
                        ultimo_lanzamiento = pygame.time.get_ticks()

                elif event.key == pygame.K_x:
                    if proyectil_cargado:
                        disparo_power.play()
                        proyectil = proyectil_personaje.ProyectilNave(nave_espacial.rect.centerx-31 , nave_espacial.rect.y-36 , misil_power_image)
                        proyectiles_lanzados_power.append(proyectil)
                        ultimo_lanzamiento = pygame.time.get_ticks()
                        
                        proyectil_cargado = False
                        barra.reiniciar_poder()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    nave_espacial.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    nave_espacial.moving_right = False
      
    # Continuar el juego normalmente
        # Bucle para aplicar cambios y mostrar.
        #movimientos de nave y enemigos
        nave_espacial.mueve()
        nave_espacial.limitar_bordes(caracteristicas.width, caracteristicas.height)
        #mover enemigos hacia abajo cada 2 segundos.
 
        #fondos e imagenes
        screen.fill((0,0, 0))
        screen.blit(nave_espacial.image, nave_espacial.rect)      
        funciones_juego.dibujar_estrellas(estrellas,screen)
        estrellas=Menu_finalizacion.mover_estrellas(estrellas)  
        #mover enemigos
        #mover balas y dibujar balas
        funciones_juego.actualizar_pnormal(proyectiles_lanzados,screen)
        funciones_juego.actualizar_ppower(proyectiles_lanzados_power,screen)
        #borras al salir del borde

        proyectiles_lanzados = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados))
        proyectiles_lanzados_power = list(filter(lambda proyectil: proyectil.rect.bottom > 0, proyectiles_lanzados_power))
        #textos
        boss.update()
        boss.draw(screen)

        boss.shoot() 

        valor_actual = puntaje.obtener()
        puntaje_texto = puntaje_font.render("Score: " + str(valor_actual), True, colores.NARANJA)
        screen.blit(scoreboard, (10, 10))
        screen.blit(puntaje_texto, (115, 43))
        screen.blit(tope_texto, (20, 300))
        #colisiones + funciones de colisiones

        explosion.update()
        explosion.draw(screen)

        colision_boss=colisiones.detectar_colisiones_boss(proyectiles_lanzados,boss,explosion,puntaje,2,barra)
        colisiones.detectar_colisiones_nave(nave_espacial, boss,puntaje,explosion)

        if colision_boss:
            dead.play()

        # Actualiza las animaciones de explosiones
        # Dibuja las explosiones en la pantalla 
        #actualizacion de barra de poder

        barra.dibujar(screen,colores.NARANJA)
        proyectil_cargado=funciones_juego.barra_poder_cargada(barra)
        
        #disparos de enemigos con recarga de tiempo


        #desaparecer misilesenemigos si sobrepasan la pantlla

        #mostrar cambios
        #dibujar o sacar vidas
        funciones_juego.vidas_pantalla(nave_espacial,nave_espacial_image_vidas,screen)
        tiempo_restante = funciones_juego.mostrar_temporizador(screen, duracion_temporizador, caracteristicas.width // 2, 0, fuente, colores.NARANJA,tiempo_inicial)

        if boss.vida == 0:
            levelup.play()
            bonus_puntos=300        
            puntuaciones["nivel_3"] = valor_actual+bonus_puntos+tiempo_restante
            puntuacion_total = sum(puntuaciones.values())
            nivel += 1
            mostrar_menu_reinicio(puntuacion_total)

        pygame.display.flip()

        if nave_espacial.obtener_vidas()==0:
            pygame.mixer.music.stop()
            gameover.play()
            puntuaciones["nivel_3"] = valor_actual
            puntuacion_total = sum(puntuaciones.values())
            mostrar_menu_reinicio(puntuacion_total)
    pygame.quit()


def cargar_nivel(nivel):
    if nivel == 1:
        jugar()
    elif nivel == 2:
        menu.pantalla_previa(2,jugar2)
    elif nivel==3:
        menu.pantalla_previa(3,jugar3)



def mostrar_menu_reinicio(puntaje):
    explosione = pygame.sprite.Group()
    frames_explosion = explosiones.cargar_imagenes_explosion(1800, 1800)
    menu_font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", 45)
    screen = pygame.display.set_mode((caracteristicas.width, caracteristicas.height))
    
    opciones = [" reiniciar ", " continuar "]
    selected_option = 0
    explosion = Explosion(caracteristicas.width // 2, caracteristicas.height // 2, frames_explosion)
    explosione.add(explosion)
    opcion_image = pygame.image.load("PYGAME/asset_opcion.png")
    opcion_image = pygame.transform.scale(opcion_image, (500,200))
    text_size=100
    game_over_font = pygame.font.Font("PYGAME/ARCADECLASSIC.TTF", text_size)
    game_over_text = game_over_font.render("Game Over", True, colores.MAGENTA)
    while True:
        screen.fill((0, 0,0))
        screen.blit(opcion_image, (710, 440))
        screen.blit(opcion_image, (710, 560))
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
                            jugar()
                            pygame.quit()  # Función para comenzar el juego
                        if selected_option == 1:
                            Menu_finalizacion.mostrar_menu_finalizacion(puntaje)
        explosione.update()
        explosione.draw(screen)
        for i, opcion in enumerate(opciones):
            if opcion != "":
                text = menu_font.render(opcion, True, (255, 255, 255) if i != selected_option else colores.MAGENTA)
                text_rect = text.get_rect(center=((caracteristicas.width / 2, caracteristicas.height / 2 + i * 110)))
                screen.blit(text, text_rect)

        
        screen.blit(game_over_text, (730,200))

        pygame.display.flip()



menu.mostrar_menu(1,jugar)