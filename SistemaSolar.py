# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 11:37:32 2016

@author: eridanus
"""

import pygame, sys
from pygame.locals import *   #constantes de pygames
import numpy as np
import pyastrolib

pygame.init()#siempre antes de usar cualquier funcion de pygames
#inicializarlo antes porque todo el resto usa cosas de juegos

###############################################################################
#                   Constantes, variables previas
###############################################################################
size_pantalla=(900,480)
centro=np.array(size_pantalla)/2
FPS=30.0

#_______________Colores______________________
DARK=(0,0,0)

#_______________Sistema solar inicial___________
sistema=pyastrolib.c_sistema([pyastrolib.Sol,pyastrolib.Tierra, pyastrolib.Jupiter],pyastrolib.posinicial,pyastrolib.velinicial)
dtcalc,sdtcalc=sistema.Estima_Delay_Calculos(1000)  #Estima el tiempo que le lleva hacer los calculos y la desviación estandar
tscale=0.01                                   #nos dice cuantos segundos son un año
rscale=70                                   #cuantos pixels son 1UA o la unidad que se elija
Ncalc=int(1.0/FPS/(dtcalc+sdtcalc))            #numero de calculos entre visualizacions
dt=1.0/FPS/Ncalc

sistema=pyastrolib.c_sistema([pyastrolib.Sol,pyastrolib.Tierra, pyastrolib.Jupiter],pyastrolib.posinicial,pyastrolib.velinicial)


###############################################################################
#                   Constantes y cosas del juego
###############################################################################

fpsClock=pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode(size_pantalla, 0, 32)#para definir el tamaño de la ventana
pygame.display.set_caption("Sistema solar")#titulo a la ventana

#________________Musica______________________
#pygame.mixer.music.load("Background.mp3")


#pygame.draw.circle(DISPLAYSURF,color,pos,radio,0)
###############################################################################
#                   El juego en si
###############################################################################

while True:#loop principal del juego
    #____________Dibuja los astros___________________
    DISPLAYSURF.fill(DARK)                          #pinta el espacio profundo
    for astro in sistema.astros:
        DISPLAYSURF.blit(astro.imagen,centro+rscale*astro.pos[0:2]-10)        #solo coordenadas xy de la posicion    
    
    #________________Control de eventos_______________
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()#sale de pygame
            sys.exit()#sale del programa
    
    pygame.display.update()

    #__________calculos______________ 
    for i in range(Ncalc):
        sistema.Movimiento(dt)
    
    fpsClock.tick(FPS)
    
    
