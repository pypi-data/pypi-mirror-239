from typing import Any

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class MontecarloIntegral:
    """
    Clase para calcular el valor de una integral por el método de Montecarlo 
    a y b: Intervalo donde está definida la función
    funcion: función a evaluar
    N: numero de puntos 
    """
    def __init__(self,a:float,b:float,funcion,N:int = 1000000):
        try:
            # Comprobar que los datos ingresados sean del tipo correcto
            a = float(a)
            b = float(b)
            N = int(N)

            # Comprobar que se puede llamar a la función
            funcion(a)
            funcion(b)

        except:
            print("Error en los datos ingresados")
            exit()
        
        self.a = a
        self.b = b
        self.N = N
        self.funcion = funcion
    
    def area(self) -> float:
        """
        Método para calcular el valor de la integral
        """
        # Calcular N punto aleatorios en el intervalo
        puntos = np.random.random(self.N)*(self.b-self.a) + self.a
        try:
            # Calcular el valor de la funcion para cada punto
            # y calcular el valor de la integral
            val_Area = self.funcion(puntos).mean()*(self.b-self.a)
        
        except ZeroDivisionError:
            print("Hay una división por cero en el intervalo ingresado")
            exit()

        return val_Area



class Kernel:

    def __init__(self) -> None:
        """
        Clase para suavizar un conjunto de datos discretos
        """
        pass

    def suavizado(self,x,y,kernel,r) -> float:
        """
        Método para calcular la funcion
             x: Datos eje x
             y: Datos eje y
        kernel: funcion
             r: r
        """
        self.x = x
        self.y = y

        N = len(x)
        self.sol = np.zeros(N)

        for i in range(N):
            sol_temp = kernel(np.arange(N),i,self.y.iloc[i],r)
            self.sol += sol_temp
        
        self.sol = self.sol/max(self.sol)

    def grafica(self,nombre="Grafica"):
        """
        Método para crear la gráfica
        nombre: nombre del archivo con la gráfica jpg
        """
        plt.plot(self.x,self.y ,label='Datos originales')
        plt.plot(self.x,self.sol,label='Datos suavizados')
        plt.xticks(rotation=45)
        plt.title('{}'.format(nombre))
        plt.legend()

        plt.savefig("{}.jpg".format(nombre))