import pygame
import random

# Dimensiones de la ventana
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TAMANIO_BLOQUE = 30

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
NARANJA = (255, 165, 0)

# Matriz del tablero
TABLERO_ANCHO = ANCHO_VENTANA // TAMANIO_BLOQUE
TABLERO_ALTO = ALTO_VENTANA // TAMANIO_BLOQUE

# Piezas del tetris
PIEZAS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

def crear_tablero_vacio():
    return [[BLANCO] * TABLERO_ANCHO for _ in range(TABLERO_ALTO)]

def dibujar_tablero(tablero):
    for fila in range(TABLERO_ALTO):
        for columna in range(TABLERO_ANCHO):
            pygame.draw.rect(ventana, tablero[fila][columna], (columna * TAMANIO_BLOQUE, fila * TAMANIO_BLOQUE, TAMANIO_BLOQUE, TAMANIO_BLOQUE))

def dibujar_pieza(pieza, posicion):
    for fila in range(len(pieza)):
        for columna in range(len(pieza[0])):
            if pieza[fila][columna]:
                pygame.draw.rect(ventana, pieza[fila][columna], ((posicion[0] + columna) * TAMANIO_BLOQUE, (posicion[1] + fila) * TAMANIO_BLOQUE, TAMANIO_BLOQUE, TAMANIO_BLOQUE))

def colisiona(pieza, posicion, tablero):
    for fila in range(len(pieza)):
        for columna in range(len(pieza[0])):
            if pieza[fila][columna] and (posicion[0] + columna < 0 or posicion[0] + columna >= TABLERO_ANCHO or posicion[1] + fila >= TABLERO_ALTO or tablero[posicion[1] + fila][posicion[0] + columna] != BLANCO):
                return True
    return False

def fijar_pieza(pieza, posicion, tablero):
    for fila in range(len(pieza)):
        for columna in range(len(pieza[0])):
            if pieza[fila][columna]:
                tablero[posicion[1] + fila][posicion[0] + columna] = pieza[fila][columna]

def eliminar_filas_completas(tablero):
    filas_completas = [fila for fila in range(TABLERO_ALTO) if BLANCO not in tablero[fila]]
    for fila in filas_completas:
        del tablero[fila]
        tablero.insert(0, [BLANCO] * TABLERO_ANCHO)

def rotar_pieza(pieza):
    return list(zip(*reversed(pieza)))

def obtener_pieza_aleatoria():
    return random.choice(PIEZAS)

def mostrar_pantalla_introducir_nombre(puntuacion):
    ventana.fill(NEGRO)
    fondo = pygame.image.load("fondo2.png")
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo, (0, 0))

    font = pygame.freetype.SysFont(None, 48)
    font.render_to(ventana, (ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 100), "¡Perdiste!", ROJO)
    font.render_to(ventana, (ANCHO_VENTANA // 2 - 160, ALTO_VENTANA // 2), "Ingresa tu nombre:", ROJO)

    nombre = ""
    nombre_ingresado = False

    while not nombre_ingresado:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    nombre_ingresado = True
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    nombre += event.unicode

        ventana.fill(NEGRO)  # Limpiar la pantalla antes de redibujar el nombre
        ventana.blit(fondo, (0, 0))  # Volver a dibujar el fondo
        font.render_to(ventana, (ANCHO_VENTANA // 2 - 75, ALTO_VENTANA // 2 + 50), nombre, VERDE)
        pygame.display.flip()  # Actualizar la pantalla

    return nombre, puntuacion


pygame.init()

ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tetris")

reloj = pygame.time.Clock()

tablero = crear_tablero_vacio()
pieza_actual = obtener_pieza_aleatoria()
posicion_pieza = [TABLERO_ANCHO // 2 - len(pieza_actual[0]) // 2, 0]
puntuacion = 0
velocidad_pieza = 1000  # Velocidad inicial de caída de las piezas en milisegundos

game_over = False
tecla_abajo_presionada = False
tiempo_anterior = pygame.time.get_ticks()

# Esperar a que se presione cualquier tecla para iniciar
esperando_inicio = True
while esperando_inicio:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            esperando_inicio = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                posicion_pieza[0] -= 1
                if colisiona(pieza_actual, posicion_pieza, tablero):
                    posicion_pieza[0] += 1
            elif event.key == pygame.K_RIGHT:
                posicion_pieza[0] += 1
                if colisiona(pieza_actual, posicion_pieza, tablero):
                    posicion_pieza[0] -= 1
            elif event.key == pygame.K_UP:
                pieza_actual = rotar_pieza(pieza_actual)
                if colisiona(pieza_actual, posicion_pieza, tablero):
                    pieza_actual = rotar_pieza(pieza_actual)
            elif event.key == pygame.K_DOWN:
                tecla_abajo_presionada = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                tecla_abajo_presionada = False
    
    tiempo_actual = pygame.time.get_ticks()
    if tecla_abajo_presionada:
        velocidad_pieza = 100
    else:
        velocidad_pieza = 1000
    
    if tiempo_actual - tiempo_anterior >= velocidad_pieza:
        posicion_pieza[1] += 1
        if colisiona(pieza_actual, posicion_pieza, tablero):
            posicion_pieza[1] -= 1
            fijar_pieza(pieza_actual, posicion_pieza, tablero)
            eliminar_filas_completas(tablero)
            puntuacion += 10
            pieza_actual = obtener_pieza_aleatoria()
            posicion_pieza = [TABLERO_ANCHO // 2 - len(pieza_actual[0]) // 2, 0]
            if colisiona(pieza_actual, posicion_pieza, tablero):
                nombre, puntuacion = mostrar_pantalla_introducir_nombre(puntuacion)
                game_over = True
        tiempo_anterior = tiempo_actual
    
    ventana.fill(NEGRO)
    fondo = pygame.image.load("fondo2.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    ventana.blit(fondo, (0, 0))
    dibujar_tablero(tablero)
    dibujar_pieza(pieza_actual, posicion_pieza)
    
    font = pygame.font.Font(None, 36)
    texto_puntuacion = font.render("Puntuacion: " + str(puntuacion), True, ROJO)
    ventana.blit(texto_puntuacion, (10, 10))
    
    pygame.display.update()
    reloj.tick(60)

    if puntuacion >= 20:
        velocidad_pieza = 50



pygame.quit()
