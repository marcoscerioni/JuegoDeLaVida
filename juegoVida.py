import pygame
import numpy as np
import time


pygame.init()

alto, ancho  = 1000, 1000  # Ancho y largo de 1000 x 1000 pixeles
screen = pygame.display.set_mode((alto, ancho)) # Creo la pantalla del juego

bg = 25, 25, 25 # Color de fondo gris oscuro. Intensidad en c/canal de color de 25
screen.fill(bg)

# Cantidad de Celdas en eje X && eje Y
celdasX, celdasY = 50, 50

# Ancho y alto de cada una de las celdas
anchoX = ancho / celdasX
altoY = alto / celdasY

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



# Bucle de Ejecucion
while True:
	
	# En cada iteracion tengo que realizar unac copia del estado actual del juego. 
	newGameState = np.copy(gameState)

	screen.fill(bg) # Limpio info para que no se superponga
	time.sleep(0.1) 

	# Dos for que recorran el ejeX y el ejeY para cada celda generada
	for y in range(0, celdasX):
		for x in range(0, celdasY):
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
			elif gameState[x, y] == 1 and (vecinos < 2 or vecinos > 3):
				newGameState[x, y] = 0
			# Regla 2: Celula viva con menos de 2 o mas de 3 vecinos vivos, muere. 


			# Coordenadas de los rectangulos
			poly = [((x)   * anchoX,   y     * altoY),
					((x+1) * anchoX,   y     * altoY),
					((x+1) * anchoX,   (y+1) * altoY),
					((x)   * anchoX,   (y+1) * altoY)]
			if newGameState[x, y] == 0:
				pygame.draw.polygon(screen, (128, 128, 128), poly, 1) # Dibujamos celdas grises del polygono dado. 
			else:
				pygame.draw.polygon(screen, (255, 255, 255), poly, 0) # Dibujamos celdas grises del polygono dado. 

	# Actualizo el estado del juego
	gameState = np.copy(newGameState)

	pygame.display.flip() # Mostrando y actuliazando los fotogramas de la escena en c/iteracion del bucle