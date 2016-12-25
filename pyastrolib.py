# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 21:25:17 2016

@author: eridanus

#lipfrog algoritmo para gravitacion y movimiento
"""

import pygame
import numpy as np

###############################################################################
#                       Constantes y unidades
# Las unidades en als que se maneja el programa serán: UA para la distancia, Masa
#solares para la masa, y años para el tiempo.
###############################################################################
G=6.02e-11              #unidades:m³/Kg.s²  #32
MS2Kg=1.989e30          #masa solar
Kg2MS=1/MS2Kg
year2secs=365*24*60*60  #segundos en un año
secs2year=1.0/year2secs
UA2Km=1.496e8           #km en 1 UA
Km2UA=1.0/UA2Km
G=G/1000**3*Km2UA**3/(secs2year**2*Kg2MS)            #G en Masas solares, UA, años

###############################################################################
#                       Clase Planeta
###############################################################################
class c_astro:
    def __init__(self,radio,masa,image_file):
        self.radio=radio            
        self.masa=masa
        self.imagen=pygame.image.load(image_file)
        
    def Set_Init(self,pos,vel):
        self.pos=np.array(pos)                #coordenadas de posición inicial, en d
        self.vel=np.array(vel)                #velocidad inicial, es vector

    def Movimiento(self,fuerza,dt):
        #el dt debe venir de afura y es cuanto le llevo hacer el loop
        aceleracion=fuerza/self.masa    #fuerza es un vector
        self.pos=self.pos+self.vel*dt+aceleracion*dt**2/2       
        self.vel=self.vel+aceleracion*dt

        
###############################################################################
#                       Clase Sistema
###############################################################################
class c_sistema:
    def __init__(self,objetos_celestes,posinicial,velinicial):
        self.astros=objetos_celestes                #debe ser una lista de planetas
        self.N=len(objetos_celestes)                #cuantos astros hay en juego
        for i,astro in enumerate(self.astros):
            astro.Set_Init(posinicial[i],velinicial[i])              #posiciones y velocidades iniciales de los astros

    def Movimiento(self,dt):
        #_______________Calculo de las fuerzas___________________
        fuerza=np.zeros((self.N,self.N,3))       #crea la matriz de fuerzas de a pares (3 coordenadas)
        for i in range(self.N-1):                   #barre n-1 astros, salvo el ultimo que se autocompleta
            for j in range(i+1,self.N):             #barre los astros que siguen
                r=self.astros[j].pos-self.astros[i].pos       #da la distancia vectorial entre los astros, direccion i->j
                fuerza[i,j,:]=G*self.astros[i].masa*self.astros[j].masa*r/np.sum(r**2)**1.5  #fuerza gravitatoria
                fuerza[j,i,:]=-fuerza[i,j,:]
        f=np.sum(fuerza,1)          #suma las fuerzas por columnas, obtiene la fuerza neta por fila

        #_______________Actualiza el movimiento__________________
        for i,astro in enumerate(self.astros):
            astro.Movimiento(f[i],dt)

    def Estima_Delay_Calculos(self,Nprb=1000):
        """
        Esta fubncion ejecuta varias veces a movimiento y asi estima aproximadamente
        cuanto le llevará hacer cada iteración.
        Nprb son el numero de pruebas para hacer la estadistica
        """
        t=np.zeros(Nprb)
        for i in range(Nprb):
            t[i]=pygame.time.get_ticks()/1000.0   #para que este en segundos
            self.Movimiento(1)
        return np.mean(np.diff(t)),np.std(np.diff(t))

###############################################################################
#                       Planetas redefinidos
###############################################################################

Sol=c_astro(695700,1,"Sol.png")
Tierra=c_astro(6371,5.972e24*Kg2MS,"Tierra.png")
Jupiter=c_astro(6371,5.972e27*Kg2MS,"Tierra.png")

posinicial=[[0.0,0.0,0.0],[1.0,0.0,0.0],[2.0,0.0,0.0]]       #el sol esta en (0,0), en el centro, la tierra a 1UA
posinicial=np.array(map(np.array,posinicial))       #convierte a np.array y lleva a km lo que estaba en UA
velinicial=[[0.0,0.0,0.0],[0.0,-6,0.0], [0.0,3,0.0]]
velinicial=np.array(map(np.array,velinicial))


