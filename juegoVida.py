import numpy as np
import time, os, pygame
import sys


pygame.init()
pygame.display.set_caption("Juego de la vida - Marcos Cerioni")

iconPath = "./icono.ico" 
if os.path.exists(iconPath):
    icono = pygame.image.load(iconPath)
    pygame.display.set_icon(icono)



alto, ancho  = 1000, 1000  # Ancho y largo de 1000 x 1000 pixeles
screen = pygame.display.set_mode((alto, ancho)) # Creo la pantalla del juego

bg = 25, 25, 25 # Color de fondo gris oscuro. Intensidad en c/canal de color de 25
screen.fill(bg)

celdasX, celdasY = 50, 50 # Cantidad de Celdas en eje X && eje Y

anchoX = ancho / celdasX # Ancho de cada una de las celdas
altoY = alto / celdasY # Alto de cada una de las celdas

""" 
Estados de cada celda. 
Creo matriz de tamaño igual al nº de celdas.
Vivas = 1. Muertas = 0.
"""
gameState = np.zeros((celdasX, celdasY))


# Planeador (Glidder) 
gameState[1, 0] = 1
gameState[2, 1] = 1
gameState[2, 2] = 1
gameState[1, 2] = 1
gameState[0, 2] = 1

# Nave espacial pesada
gameState[19, 21] = 1
gameState[20, 21] = 1
gameState[21, 21] = 1
gameState[22, 21] = 1
gameState[23, 21] = 1
gameState[24, 21] = 1
gameState[18, 22] = 1
gameState[24, 22] = 1
gameState[24, 23] = 1
gameState[18, 24] = 1
gameState[23, 24] = 1
gameState[20, 25] = 1
gameState[21, 24] = 1

# Nave Espacial Ligera
gameState[21, 30] = 1
gameState[22, 30] = 1
gameState[23, 31] = 1
gameState[22, 31] = 1
gameState[20, 31] = 1
gameState[19, 31] = 1
gameState[19, 32] = 1
gameState[20, 32] = 1
gameState[21, 32] = 1
gameState[22, 32] = 1
gameState[20, 33] = 1
gameState[21, 33] = 1



pausarEjec = False # Control ejecucion.


iteraciones = 0 # Acumulador de cantidad de iteraciones:


while True:
    newGameState = np.copy(gameState) # Realizo una copia del estado actual del juego. 

    screen.fill(bg) # Limpio info para que no se superponga
    time.sleep(0.1) 

    ev = pygame.event.get() # Registro eventos del teclado y mouse. 

    # Contador de población
    poblacion = 0

    for event in ev:
        if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

        if event.type == pygame.KEYDOWN:
            pausarEjec = not pausarEjec

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / anchoX)), int(np.floor(posY / altoY))
            newGameState[celX, celY] = not mouseClick[2]

    if not pausarEjec:
        iteraciones += 1
    
    # Dos for que recorran el ejeX y el ejeY para cada celda generada
    for y in range(0, celdasX):
        for x in range(0, celdasY):

            if not pausarEjec:
                
                # Incremento el contador de población:
                if gameState[x, y] == 1:
                    poblacion += 1
                
                # Nº de vecinos cercanos. 
                vecinos = gameState[(x-1) % celdasX, (y-1)  % celdasY] + \
                          gameState[(x)   % celdasX, (y-1)  % celdasY] + \
                          gameState[(x+1) % celdasX, (y-1)  % celdasY] + \
                          gameState[(x-1) % celdasX, (y)    % celdasY] + \
                          gameState[(x+1) % celdasX, (y)    % celdasY] + \
                          gameState[(x-1) % celdasX, (y+1)  % celdasY] + \
                          gameState[(x)   % celdasX, (y+1)  % celdasY] + \
                          gameState[(x+1) % celdasX, (y+1)  % celdasY]

                # Regla 1: Una celula muerta con 3 vecinos vivos, revive. 
                if gameState[x, y] == 0 and vecinos == 3:
                    newGameState[x, y] = 1
                # Regla 2: Celula viva con menos de 2 o mas de 3 vecinos vivos, muere. 
                elif gameState[x, y] == 1 and (vecinos < 2 or vecinos > 3):
                    newGameState[x, y] = 0


            # Coordenadas de los rectangulos
            poly = [((x)   * anchoX,   y     * altoY),
                    ((x+1) * anchoX,   y     * altoY),
                    ((x+1) * anchoX,   (y+1) * altoY),
                    ((x)   * anchoX,   (y+1) * altoY)]
            
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                if pausarEjec:
                    pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
                else:
                    pygame.draw.polygon(screen, (255, 255, 255), poly, 0) 


    title = f"Juego de la vida - Marcos Cerioni - Población: {poblacion} - Generación: {iteraciones}"
    if pausarEjec:
        title += " - [PAUSADO]"
    pygame.display.set_caption(title)


    # Actualizo el estado del juego
    gameState = np.copy(newGameState)

    pygame.display.flip() # Mostrando y actuliazando los fotogramas de la escena en c/iteracion del bucle

