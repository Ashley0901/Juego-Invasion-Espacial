import pygame
from random import randint
import math
from pygame import mixer
#inicializamos pygme
pygame.init()

#screen and tittle
pantalla = pygame.display.set_mode((800,600))
pygame.display.set_caption("Invasión alienigena")
#icon and screen blit
icono = pygame.image.load('ovnis.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('Fondo.jpg')

#variables del player
img_player = pygame.image.load('cohete.png')
player_x = 368
player_y = 536
player_x_cambio = 0

#variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
emigo_y_cambio = []
cantidad_enemigos = 8
#loop que itera y les da atributos a cada uno de los 8 enemigos
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('enemigo.png'))
    enemigo_x.append(randint(0,736))
    enemigo_y.append(randint(50,200))
    enemigo_x_cambio.append(-1.5)
    emigo_y_cambio.append(50)

#variables de la bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 536
bala_x_cambio = 0
bala_y_cambio = 6
bala_visible = False

#puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf',20)
texto_x = 10
textto_y= 10

#musica a nuestro juego con la clase mixer del mismo modulo pygame
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(.2)
mixer.music.play(-1)

#variable para texto final
fuente_final = pygame.font.Font('freesansbold.ttf',60)

#funcino para terminar el juego con un texto final
def texto_final():
    text_final = fuente_final.render('JUEGO TERMINADO',True,(255,255,255))
    pantalla.blit(text_final,(90,200))



#funcion para marcar el puntaje
def puntuacion (x,y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto,(x,y))

#funcion para la ubicacion del jugador que nos va a servir para actualizar la ubicacion de la nave
def player(x,y):
    pantalla.blit(img_player,(x,y))

#funcion para la ubicacion del enemigo
def enemigo(x,y,enem):
    pantalla.blit(img_enemigo[enem], (x,y))

#funcion para disparar la bala
def disparar_bala(x,y):

    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x+15,y+16))

#funcion que me detecta si hay una colision entre el enemigo y la bala
def colisionar(x1,y1,x2,y2):
    distancia = math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
    if distancia<27:
        return True
    else:
        return False

se_ejecuta = True
#loop of the game
while se_ejecuta:
    '''#RGB # este codigo me cambiaba el color de la pantalla pero ahora nosotros vamos a setear un fondo
    pantalla.fill((205, 144, 228))'''
    pantalla.blit(fondo,(0,0))

    #iterar eventos
    for evento in pygame.event.get():

        #evento para cerrar el juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #evento para mover en el eje de las x nuestra nave
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                player_x_cambio += 1.5
            if evento.key == pygame.K_LEFT:
                player_x_cambio -= 1.5
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    mp3_bala = mixer.Sound('disparo.mp3')
                    mp3_bala.set_volume(.1)
                    mp3_bala.play()
                    bala_x = player_x
                    disparar_bala(bala_x,bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                player_x_cambio = 0


    # actualizacion de la ubicacion de la nave
    player_x += player_x_cambio

    #mantener dentro de los bordes a la nave
    if player_x < 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # actualizacion de la ubicacion del enemigo
    for e in range(cantidad_enemigos):

        if enemigo_y[e] >500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]
        # mantener dentro de los bordes del enemigo
        if enemigo_x[e] < 0:
            enemigo_x_cambio[e] = 1.5
            enemigo_y[e] += 50
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1.5
            enemigo_y[e] += 50

        enemigo(enemigo_x[e], enemigo_y[e],e)

        # colision del disparo con el enemigo
        colision = colisionar(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            mp3_colision = mixer.Sound('Golpe.mp3')
            mp3_colision.set_volume(.2)
            mp3_colision.play()
            bala_visible = False

            bala_y = 500
            puntaje += 1
            enemigo_x[e] = randint(0, 736)
            enemigo_y[e] = randint(50, 200)

    #disparar bala
    if bala_y<=-64:
        bala_visible = False
        bala_y = 536
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio


    #ubicacion del jugador y del enemigo
    player(player_x, player_y)

    #marco de puntaje en el lado izquierdo arriba
    puntuacion(texto_x,textto_y)

    #actualiza todos los eventos que suceden antes de cerrar el while y empezar de nuevo
    pygame.display.update()


