import pygame
import time
import subprocess
import os
from Buscaminas import gameLoop

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
pygame.mixer.init() #Inicializa el mixer de pygame
ventana=pygame.display.set_mode((565,800)) #crea la ventana


#----------------------------------------------------------
#sonido al dar click
click=pygame.mixer.Sound("Sonidos/Click.mp3")

#----------------------------------------------------------
def AbrirArchivo():
    '''
    Nombre:     AbrirArchivo

    Objetivo:   Abrir un archivo de texto con el programa predeterminado en el sistema operativo.

    Parámetros: Esta función no tiene parámetros.

    Retorno:    Esta función no devuelve ningún valor.
    '''

    archivo=("Creditos.txt")
    subprocess.run(['open', archivo]) #Para entorno Unix (Mac o Linux)
    #os.startfile(archivo) #Para entorno Windows

#----------------------------------------------------------
def intro():
    '''
    Ejecuta la introducción del juego.

    Nombre:     intro

    Objetivo:   Mostrar una introducción visual del juego durante 5 segundos antes de pasar al menú principal.

    Parámetros: Esta función no tiene parámetros.

    Retorno:    Esta función no devuelve ningún valor.
    '''

    ventana=pygame #crea la ventana
    ventana=pygame.display.set_mode((565,800)) #tamaño de la ventana
    pygame.display.set_caption("Intro") #titulo de la ventana
    imgintro=pygame.image.load("Fondos/Intro.png") #carga la imagen de la intro del juego
    ventana.blit((imgintro),(0,0)) #pone la imagen en la ventana
    pygame.display.update()
    time.sleep(3) #espera 3 segundos
    menu() #llama la funcion menu
#----------------------------------------------------------
def Ayuda():
    '''
    Nombre:     Ayuda

    Objetivo:   Mostrar la pantalla de ayuda y permitir al usuario volver al menú principal cuando hace clic en un botón específico.

    Parámetros: Esta función no tiene parámetros.

    Retorno:    Esta función no devuelve ningún valor.
    '''

    ventana = pygame #crea la ventana
    ventana = pygame.display.set_mode((565,800)) #tamaño de la ventana
    pygame.display.set_caption("Ayuda") #titulo de la ventana
    Ayuda = pygame.image.load("Fondos/Ayuda.png") #carga la imagen de las instrucciones del juego
    ventana.blit(Ayuda, (0,0)) #pone la imagen en la ventana
    pygame.display.update()
    while True:
        for Eventos in pygame.event.get():
            if Eventos.type==pygame.QUIT: #si se da click en la x de la ventana
                exit()
            if Eventos.type ==pygame.MOUSEBUTTONDOWN: #si se da click
                if Eventos.button==1: #si se da click izquierdo
                    x,y = Eventos.pos #posicion del mouse
                    if x>153 and x<411 and y>669 and y<765: #si se da click en el boton volver para regresar al menu
                        click.play()
                        menu() #llama la funcion menu
#----------------------------------------------------------
def Creditos():
    '''
    Nombre:     Creditos

    Objetivo:   Mostrar la pantalla de créditos y permitir al usuario volver al menú principal cuando hace clic en un botón específico.

    Parámetros: Esta función no tiene parámetros.

    Retorno:    Esta función no devuelve ningún valor.
    '''

    ventana = pygame #crea la ventana
    ventana = pygame.display.set_mode((565,800)) #tamaño de la ventana
    pygame.display.set_caption("Créditos") #titulo de la ventana
    Creditos = pygame.image.load("Fondos/Creditos.png") #carga la imagen de los creditos del juego
    ventana.blit(Creditos, (0,0)) #pone la imagen en la ventana
    pygame.display.update()
    while True:
        for Eventos in pygame.event.get():
            if Eventos.type==pygame.QUIT: #si se da click en la x de la ventana
                exit()
            if Eventos.type == pygame.MOUSEBUTTONDOWN: #si se da click
                if Eventos.button==1: #si se da click izquierdo
                    x,y = Eventos.pos #posicion del mouse
                    if x>153 and x<411 and y>669 and y<765: #si se da click en el boton volver para regresar al menu
                        click.play()
                        menu()

#----------------------------------------------------------
def menu():
    '''
    Nombre:     menu

    Objetivo:   Mostrar el menú principal y permitir al usuario seleccionar diferentes opciones.

    Parámetros: Esta función no tiene parámetros.

    Retorno:    Esta función no devuelve ningún valor.
    '''

    ventana=pygame.display.set_mode((565,800)) #tamaño de la ventana
    pygame.display.set_caption("Menu") #titulo de la ventana
    imgMenu=pygame.image.load("Fondos/Menu.png") #carga la imagen del menu del juego
    ventana.blit((imgMenu),(0,0)) #pone la imagen en la ventana
    pygame.display.update()
    
    while True:
        for eventos in pygame.event.get():
            if eventos.type==pygame.QUIT: #si se da click en la x de la ventana
                exit()
            if eventos.type==pygame.MOUSEBUTTONDOWN:
                if eventos.button==1: #si se da click izquierdo
                    x,y=eventos.pos
                    if x>0 and x<565 and y>0 and y<800: #para verificar si se da click dentro de la ventana
                        if x>154 and x<413 and y>235 and y<331: #si se da click en el boton ayuda
                            #print("AYUDA")
                            click.play()
                            Ayuda() #llama la funcion ayuda
                        if x>156 and x<416 and y>346 and y<443: #si se da click en el boton jugar
                            #print("JUGAR")
                            click.play()
                            gameLoop(0) #Llama al bucle principal del juego, indicando que no se ha realizado un click inicial
                            ventana.blit((imgMenu),(0,0)) #vuelve al menu inmediatamente
                        if x>154 and x<413 and y>465 and y<561: #si se da click en el boton salir
                            #print("SALIR")
                            click.play()
                            time.sleep(1) #esperar 1 segundo antes de cerrar la ventana
                            exit()
                        if x>154 and x<413 and y>583 and y<679: #si se da click en el boton creditos
                            #print("CRÉDITOS")
                            click.play()
                            AbrirArchivo() #llama la funcion AbrirArchivo para mostrar el archivo de texto que incluye los links de los sonidos utilizados en el programa
                            Creditos() #llama la funcion creditos

            pygame.display.update()
            ventana.blit((imgMenu),(0,0))   

intro()