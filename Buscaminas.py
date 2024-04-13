import pygame
import random

'''
Autores: Jennifer Quintana y Melissa Henao
Asignatura: Computación Grafica
Fecha: 07/06/2023
DESCRIPCION: Este programa es un juego de buscaminas, en el cual el usuario debe encontrar las minas
que se encuentran en el tablero, para esto debe ir destapando las casillas, si destapa una mina pierde,
si destapa una casilla vacia, se le mostrara el numero de minas que hay alrededor de esa casilla. Si da
clic derecho, puede poner una bandera cuando tenga sospecha de que hay una mina en la casilla.
'''

pygame.init()

anchoTablero = 8
altoTablero = 8
numMinas = 10  #Numero de minas
casilla = 51  #Tamaño de cada casilla
borde = 79  #Distancia entre los lados del tablero y la ventana
bordeSup = 183  #Distancia entre parte superior de ventana y tablero
anchoVentana = 565
altoVentana = 800
ventana = pygame.display.set_mode((anchoVentana, altoVentana))  #Crear ventana
reloj = pygame.time.Clock()  #Crear reloj
fuente = pygame.font.SysFont("Times New Roman", 35)
fuente2 = pygame.font.SysFont("Times New Roman", 30, True)
pygame.display.set_caption("Buscaminas")  #Nombre de la ventana

#Imagenes del tablero
figCasillaVacia = pygame.image.load("Figuras/Empty.png")
figBandera = pygame.image.load("Figuras/Flag.png")
figCasillaCubierta = pygame.image.load("Figuras/Covered.png")
figClue1 = pygame.image.load("Figuras/Clue1.png")
figClue2 = pygame.image.load("Figuras/Clue2.png")
figClue3 = pygame.image.load("Figuras/Clue3.png")
figClue4 = pygame.image.load("Figuras/Clue4.png")
figClue5 = pygame.image.load("Figuras/Clue5.png")
figClue6 = pygame.image.load("Figuras/Clue6.png")
figClue7 = pygame.image.load("Figuras/Clue7.png")
figClue8 = pygame.image.load("Figuras/Clue8.png")
figMine = pygame.image.load("Figuras/Mine.png")
figMineFound = pygame.image.load("Figuras/MineFound.png")
figFalseMine = pygame.image.load("Figuras/FalseMine.png")
    
#Musica
sonidoFondo = pygame.mixer.Sound("Sonidos/Fondo.mp3") #Musica de fondo
efecto = pygame.mixer.Sound("Sonidos/MineFound.flac")
click = pygame.mixer.Sound("Sonidos/Click.mp3")

#Mensajes
gameOver = pygame.image.load("Mensajes/GameOver.png")
Win = pygame.image.load("Mensajes/Win.png")

#Listas para las casillas y las minas
grid = []  #Para almacenar las información de cada casilla
mines = []  #Para almacenar las posiciones de las minas

#Clase que crea las casillas
class Casilla:
    '''
    Nombre:     Casilla

    Objetivo:   Representar una casilla del juego de buscaminas.

    Parámetros:
        - xCasilla (int):    Posición X de la casilla en el tablero.
        - yCasilla (int):    Posición Y de la casilla en el tablero.
        - type (int):        Valor de la casilla, donde -1 indica una mina y cualquier otro valor indica una casilla vacía o una pista.

    Atributos:
        - xCasilla (int):        Posición X de la casilla en el tablero.
        - yCasilla (int):        Posición Y de la casilla en el tablero.
        - clicked (bool):        Bandera para verificar si la casilla fue clickeada.
        - mineFound (bool):      Bandera para verificar si la casilla fue clickeada y si es una mina.
        - FalseMine (bool):      Bandera para verificar si el jugador puso una bandera incorrectamente.
        - flag (bool):           Bandera para verificar si el jugador puso una bandera en la casilla.
        - rectCasilla (pygame.Rect):  Rectángulo que representa la posición y tamaño de la casilla en la pantalla.
        - valorCasilla (int):    Valor de la casilla, donde -1 indica una mina y cualquier otro valor indica una casilla vacía o una pista.

    Métodos:
        - dibujarCasilla(self):    Dibuja la casilla en la pantalla de acuerdo con las banderas booleanas y el valor de la casilla.
        - revelarCasilla(self):    Revela la casilla en el juego y, en caso de ser necesario, revela las casillas adyacentes si la casilla es vacía.
        - actualizarValor(self):   Actualiza el valor de la casilla en función del número de minas adyacentes.
    '''

    def __init__(self, xCasilla, yCasilla, type):
        self.xCasilla = xCasilla  #Posición X de la casilla
        self.yCasilla = yCasilla  #Posición Y de la casilla
        self.clicked = False  #Bandera para verificar si la casilla fue clickeada
        self.mineFound = False  #Bandera para verificar si la casilla fue clickeada y si es una mina
        self.FalseMine = False  #Bandera para verificar si el jugador puso una bandera incorrectamente
        self.flag = False  #Bandera para verificar si el jugador puso una bandera en la casilla
            
        #Creación de objetos para dibujar y hacer las colisiones
        self.rectCasilla = pygame.Rect(borde + self.xCasilla * casilla, bordeSup + self.yCasilla * casilla, casilla, casilla)
        self.valorCasilla = type  #Valor de la casilla, si es -1 es una mina

    def dibujarCasilla(self):
        '''
        Nombre:     dibujarCasilla

        Objetivo:   Dibujar la casilla en la pantalla de acuerdo con las banderas booleanas y el valor de la casilla.

        Parámetros:
            - self (objeto): La instancia de la clase que invoca el método.

        Retorno:    Este método no devuelve ningún valor.
        '''

        #Dibuja la casilla basado en las banderas booleanas y el valor de la casilla
        if self.FalseMine:
            ventana.blit(figFalseMine, self.rectCasilla)
        else:
            if self.clicked:
                if self.valorCasilla == -1: #Si el valor de la casilla clickeada es -1
                    if self.mineFound: #Se verifica si el jugador encontró una mina
                        ventana.blit(figMineFound, self.rectCasilla) #Se dibuja la mina encontrada
                    else: #Si no la encontró el jugador, se dibuja la mina normal
                        ventana.blit(figMine, self.rectCasilla)
                else: #Si no es una mina, entonces es una casilla vacía o una pista. Por ende, se dibuja la imagen correspondiente
                    if self.valorCasilla == 0: #No hay minas adyacentes, entonces casilla vacía
                        ventana.blit(figCasillaVacia, self.rectCasilla)
                    elif self.valorCasilla == 1: #Una mina adyacente
                        ventana.blit(figClue1, self.rectCasilla)
                    elif self.valorCasilla == 2: #Dos minas adyacentes
                        ventana.blit(figClue2, self.rectCasilla)
                    elif self.valorCasilla == 3: #Tres minas adyacentes
                        ventana.blit(figClue3, self.rectCasilla)
                    elif self.valorCasilla == 4: #Cuatro minas adyacentes
                        ventana.blit(figClue4, self.rectCasilla)
                    elif self.valorCasilla == 5: #Cinco minas adyacentes
                        ventana.blit(figClue5, self.rectCasilla)
                    elif self.valorCasilla == 6: #Seis minas adyacentes
                        ventana.blit(figClue6, self.rectCasilla)
                    elif self.valorCasilla == 7: #Siete minas adyacentes
                        ventana.blit(figClue7, self.rectCasilla)
                    elif self.valorCasilla == 8: #Ocho minas adyacentes
                        ventana.blit(figClue8, self.rectCasilla)

            else: #Si no se hizo click para revelar una casilla
                if self.flag: #Si se puso una bandera
                    ventana.blit(figBandera, self.rectCasilla)
                else: #Si no se hizo click ni se puso bandera, entonces es una casilla cubierta
                    ventana.blit(figCasillaCubierta, self.rectCasilla)

    def revelarCasilla(self):
        '''
        Nombre:     revelarCasilla

        Objetivo:   Revelar la casilla en el juego y, en caso de ser necesario, revelar las casillas adyacentes si la casilla es vacía.

        Parámetros: self (objeto): La instancia de la clase que invoca el método.

        Retorno:    Este método no devuelve ningún valor.
        '''

        #Revela la casilla basado en el valor de la casilla

        self.clicked = True #Se establece que la casilla fue clickeada
            
        #Si la casilla es 0, significa que está vacía (no tiene minas adyacentes), entonces se revelan las casillas vecinas
        if self.valorCasilla == 0:
            for xCasillaActual in range(-1, 2): #Se verifican las columnas adyacentes a la actual
                if self.xCasilla + xCasillaActual >= 0 and self.xCasilla + xCasillaActual < anchoTablero: #Revisar que esté en el rango del tablero
                    for yCasillaActual in range(-1, 2): #Se verifican las filas adyacentes a la actual
                        if self.yCasilla + yCasillaActual >= 0 and self.yCasilla + yCasillaActual < altoTablero: #Revisar que esté en el rango del tablero
                            if not grid[self.yCasilla + yCasillaActual][self.xCasilla + xCasillaActual].clicked: #Si la casilla adyacente no ha sido clickeada
                                grid[self.yCasilla + yCasillaActual][self.xCasilla + xCasillaActual].revelarCasilla() #Se llama a si misma para revelar la casilla
        #Si la casilla es -1, hay una mina y se deben revelar todas las minas
        elif self.valorCasilla == -1:
            for m in mines: #Se recorren las minas de la lista de minas
                if not grid[m[1]][m[0]].clicked: #Verificar si la casilla de esa mina fue la clickeada
                    grid[m[1]][m[0]].revelarCasilla() #Se llama a si misma para revelar la casilla

    def actualizarValor(self):
        '''
        Nombre:     actualizarValor

        Objetivo:   Actualizar el valor de la casilla en función del número de minas adyacentes.

        Parámetros:
            - self (objeto): La instancia de la clase que invoca el método.

        Retorno:    Este método no devuelve ningún valor.
        '''

        #Actualiza el valor de la casilla basado en el numero de minas adyacentes
        if self.valorCasilla != -1: #Se verifica que no sea una mina para no cambiar su valor
            for xCasillaActual in range(-1, 2): #Se verifican las columnas adyacentes a la actual
                if self.xCasilla + xCasillaActual >= 0 and self.xCasilla + xCasillaActual < anchoTablero: #Revisar que esté en el rango del tablero
                    for yCasillaActual in range(-1, 2): #Se verifican las filas adyacentes a la actual
                        if self.yCasilla + yCasillaActual >= 0 and self.yCasilla + yCasillaActual < altoTablero: #Revisar que esté en el rango del tablero
                            if grid[self.yCasilla + yCasillaActual][self.xCasilla + xCasillaActual].valorCasilla == -1: #Verifica si la casilla adyacente tiene una mina
                                self.valorCasilla += 1

#Bucle del juego
def gameLoop(clickInicial):
    '''
    Nombre:     gameLoop

    Objetivo:   Controlar el flujo principal del juego, incluyendo la generación del tablero, la interacción con el jugador,
                el cálculo del puntaje y la verificación de las condiciones de victoria o derrota.

    Parámetros:
        - clickInicial (int):   Valor que indica si ha ocurrido un clic inicial. Se utiliza para evitar interacciones
                                antes de que el jugador realice el primer clic. El valor 0 indica que no se ha realizado
                                un clic inicial, mientras que cualquier otro valor indica que sí se ha realizado.

    Retorno:    Este método no devuelve ningún valor explícito.
    '''

    gameState = "Jugando"  #Estado actual del juego
    sonidoFondo.play(-1)#-1 para que se repita la musica
    minasRestantes = numMinas  #Numero de minas restantes, inicialmente son el total de minas en el juego
    global grid  #Se accede a la variable global que hace referencia a las casillas
    grid = [] #Para almacenar la información del tablero
    global mines #Se accede a la variable global que hace referencia a las minas
    tiempo = 0  #Se inicializa el tiempo en 0
    score = 0 #Puntaje inicial en 0

    #Se generan las minas en una posición aleatoria dentro del tablero
    mines = [[random.randrange(0, anchoTablero), random.randrange(0, altoTablero)]]

    for mina in range(numMinas - 1): #Se recorre la cantidad de minas del juego
        #Se genera una posición aleatoria para la mina
        pos = [random.randrange(0, anchoTablero), random.randrange(0, altoTablero)]
        posRepetida = True #Significa que aun no se verifica que sea una pos unica para la mina
        while posRepetida:
            for mina in range(len(mines)): #Se recorre cada pos de la lista de minas
                if pos == mines[mina]:
                    pos = [random.randrange(0, anchoTablero), random.randrange(0, altoTablero)] #Se asigna una nueva pos a la mina
                    break
                if mina == len(mines) - 1: #Si ya llegamos a la ultima mina, no necesitamos mirar si está repetida la pos
                    posRepetida = False
        mines.append(pos)

    #Generar el tablero completo
    for row in range(altoTablero): #Recorre las filas del tablero
        fila = [] #Representa una fila del tablero
        for col in range(anchoTablero): #Recorre las columnas del tablero
            if [col, row] in mines: #Si esa casilla es de una mina
                fila.append(Casilla(col, row, -1)) #Se crea el objeto de la casilla sabiendo que es una mina y se agrega a la fila
            else: #Si la casilla no es de una mina
                fila.append(Casilla(col, row, 0)) #Se crea el objeto de la casilla sabiendo que no es una mina y se agrega a la fila
        grid.append(fila) #Se agrega la fila a la lista del tablero

    #Actualización de valores de las casillas después de tener las minas ubicadas
    for fila in grid:
        for casilla in fila:
            casilla.actualizarValor()

    #Bucle principal del juego
    while gameState != "Cerrar":
        # Reset screen
        ventana.blit(fondoJugar, (0, 0))  #Se dibuja la imagen de fondo
        pygame.display.set_caption("Jugar")

        #Entradas del jugador
        for event in pygame.event.get():
            #Verificar si el jugador cerró la ventana
            if event.type == pygame.QUIT:
                gameState = "Cerrar"
                sonidoFondo.stop()
            #Verificar si el jugador reinició el juego o volvió al menu
            if gameState == "Game Over" or gameState == "Win":
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x,y=event.pos
                        if x>0 and x<565 and y>0 and y<800:
                            if x>12 and x<270 and y>680 and y<776:
                                #print("Reiniciar")
                                click.play()
                                gameState = "Cerrar"
                                sonidoFondo.play(-1)
                                gameLoop(0)
                            if x>293 and x<551 and y>680 and y<776:
                                gameState = "Cerrar"
                                click.play()
                                sonidoFondo.stop()
                                #print("Volver")
                                pygame.display.set_caption("Menu")
            #Verificar si el jugador hizo click
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y=event.pos
                    if clickInicial != 0:
                        if x>0 and x<565 and y>0 and y<800:
                            if x>12 and x<270 and y>680 and y<776:
                                #print("Reiniciar")
                                click.play()
                                gameState = "Cerrar"
                                sonidoFondo.stop()
                                gameLoop(0)
                            if x>293 and x<551 and y>680 and y<776:
                                gameState = "Cerrar"
                                click.play()
                                sonidoFondo.stop()
                                #print("Volver")
                                pygame.display.set_caption("Menu")
                        for fila in grid:
                            for casilla in fila:
                                if casilla.rectCasilla.collidepoint(event.pos): #Verifica si el click fue dentro de la casilla
                                    if event.button == 1: #Si hace click izquierdo
                                        casilla.revelarCasilla() #Revela el contenido de la casilla
                                        if casilla.flag: #Si la casilla tiene una bandera
                                            minasRestantes += 1 #Aumenta el contador de minas
                                            casilla.flag = False #Quita la bandera
                                        if casilla.valorCasilla == -1: #Si la casilla es de una mina
                                            gameState = "Game Over" #Pierde
                                            casilla.mineFound = True #Indica que la mina encontrada es la de esa casilla
                                            efecto.play()
                                            sonidoFondo.stop()
                                    elif event.button == 3: #Si hace click derecho
                                        if not casilla.clicked: #Si la casilla no ha sido clickeada (revelada)
                                            if casilla.flag: #Si hay una bandera en esa casilla
                                                casilla.flag = False #Quita la bandera
                                                minasRestantes += 1 #Aumenta el contador de minas
                                            else: #Si no hay una bandera, la pone y disminuye la cantidad de minas restantes
                                                casilla.flag = True
                                                minasRestantes -= 1
                    else:
                        clickInicial = 1

        #Verificar si se ganó
        win = True
        for fila in grid:
            for casilla in fila:
                casilla.dibujarCasilla()
                if casilla.valorCasilla != -1 and not casilla.clicked: #Se verifica si hay una casilla sin revelar que no sea una mina
                    win = False
        if win and gameState != "Cerrar":
            gameState = "Win"

        #Mostrar los mensajes
        if gameState == "Game Over": #Si se perdió
            #Calcular puntaje
            T = tiempo/30
            if T < 10:
                score = 10
            else:
                score = 100
            ventana.blit(gameOver, (32, 5)) #Se muestra el mensaje de game over
            mensajeScoreGO = fuente.render(str(score),True,(255,255,255))
            mensajeTiempoGO = fuente.render(str(int(T)) + " s",True,(255,255,255))
            ventana.blit(mensajeTiempoGO,(320, 95)) #Se agrega el tiempo al mensaje
            ventana.blit(mensajeScoreGO,(320, 130)) #Se agrega el puntaje al mensaje
            for fila in grid:
                for casilla in fila:
                    if casilla.flag and casilla.valorCasilla != -1: #Se verifica si se marcó erroneamente una bandera
                        casilla.FalseMine = True
        elif gameState == "Win": #Si se ganó
            #Calcular puntaje
            T = tiempo/30
            if T < 30:
                score = 1000
            elif T >= 30 and T < 60:
                score = 900
            elif T >= 60 and T < 100:
                score = 700
            elif T >= 100 and T < 160:
                score = 500
            elif T >= 160 and T < 210:
                score = 300
            else:
                score = 200
            ventana.blit(Win, (32, 5)) #Se muestra el mensaje de win
            mensajeScoreW = fuente.render(str(score),True,(255,255,255))
            mensajeTiempoW = fuente.render(str(int(T)) + " s",True,(255,255,255))
            ventana.blit(mensajeTiempoW,(320, 95)) #Se agrega el tiempo al mensaje
            ventana.blit(mensajeScoreW,(320, 130)) #Se agrega el puntaje al mensaje
        else: #Si se está jugando
            mensajeMinas = fuente2.render(str(minasRestantes),True,(0,0,0))
            ventana.blit(mensajeMinas,(80, 120)) #Se muestra la cantidad de minas
            mensajeTiempoJ = fuente2.render(str(int(tiempo/30)) + " s",True,(0,0,0))
            ventana.blit(mensajeTiempoJ,(430, 120)) #Se muestra el tiempo

            #Actualizar ventana y aumentar el tiempo
            pygame.display.update()
            reloj.tick(30)
            tiempo += 1

        pygame.display.update()

#Empezar el juego
fondoJugar = pygame.image.load("Fondos/Jugar.png")