import pygame
import numpy as np
import time


pygame.init()

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


# Ejemplo en donde se va moviendo. 
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

pausarEjec = False # Control ejecucion.

# Bucle de Ejecucion
while True:
	newGameState = np.copy(gameState) # Realizo una copia del estado actual del juego. 

	screen.fill(bg) # Limpio info para que no se superponga
	time.sleep(0.1) 

	ev = pygame.event.get() # Registro eventos del teclado y mouse. 

	for event in ev:
		if event.type == pygame.KEYDOWN:
			pausarEjec = not pausarEjec

		mouseClick = pygame.mouse.get_pressed()
		if sum(mouseClick) > 0:
			posX, posY = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posX / anchoX)), int(np.floor(posY / altoY))
			newGameState[celX, celY] = not mouseClick[2]

	# Dos for que recorran el ejeX y el ejeY para cada celda generada
	for y in range(0, celdasX):
		for x in range(0, celdasY):

			if not pausarEjec:
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
				pygame.draw.polygon(screen, (255, 255, 255), poly, 0) 

	# Actualizo el estado del juego
	gameState = np.copy(newGameState)

	pygame.display.flip() # Mostrando y actuliazando los fotogramas de la escena en c/iteracion del bucle