
from explosiones import Explosion
import explosiones

frames_explosion = explosiones.cargar_imagenes_explosion(55,44)


def detectar_colisiones(proyectiles, enemigos, barra_poder, puntos, explosiones):
    colision = False  # Variable para indicar si se produce una colisión

    for proyectil in proyectiles:
        for enemigo in enemigos:
            if enemigo.rect.colliderect(proyectil.rect):
                enemigos.remove(enemigo)
                proyectiles.remove(proyectil)
                barra_poder.aumentar_poder()
                puntos.aumentar(20)
                # Crear una instancia de la clase Explosion y agregarla a la lista temporal
                explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, frames_explosion)
                explosiones.add(explosion)
                colision = True  # Se produce una colisión
                break

    return colision

  
def detectar_colisiones_power(proyectiles, enemigos,explosiones,puntos):
     colision=False
     for proyectil in proyectiles:
        for enemigo in enemigos:
            if enemigo.rect.colliderect(proyectil.rect):
                explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery,frames_explosion)
                explosiones.add(explosion)
                puntos.aumentar(15)
                enemigos.remove(enemigo)
                colision=True
                break
        return colision
frames_explosion_nave = explosiones.cargar_imagenes_explosion(60,60)

def detectar_colisiones_enemigas(proyectiles,personaje,explosiones,puntos):
    colision=False
    for proyectil in proyectiles:
        if personaje.rect.colliderect(proyectil.rect):
            proyectiles.remove(proyectil)
            personaje.restar_vida()
            puntos.restar(50)
            explosion = Explosion(personaje.rect.centerx, personaje.rect.centery,frames_explosion_nave)
            explosiones.add(explosion)
            colision=True

        return colision
    
def detectar_colisiones_boss(proyectiles,boss,explosiones,puntos,resto,barra_poder):
        colision=False
        for proyectil in proyectiles:
            if boss.rect.colliderect(proyectil.rect):
                proyectiles.remove(proyectil)
                boss.restar_vida(resto)
                puntos.aumentar(30)
                barra_poder.aumentar_poder()

                explosion = Explosion(boss.rect.centerx, boss.rect.centery,frames_explosion_nave)
                explosiones.add(explosion)
                colision=True

            return colision
def detectar_colisiones_nave(personaje, boss,puntos,explosiones):
    if boss.boss_proyectil is not None:
        if personaje.rect.colliderect(boss.boss_proyectil.rect):
            
            boss.visible = False
            personaje.restar_vida()
            personaje.restar_vida()
            personaje.restar_vida()
            puntos.restar(50)
            explosion = Explosion(personaje.rect.centerx, personaje.rect.centery,frames_explosion_nave)
            explosiones.add(explosion)
            

        

