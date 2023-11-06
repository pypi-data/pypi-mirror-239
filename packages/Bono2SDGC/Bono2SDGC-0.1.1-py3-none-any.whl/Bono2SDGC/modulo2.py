import numpy as np
import pandas as pd
import datetime as datetime
import matplotlib.pyplot as plt

class Ajuste:
    """ 
    Ajuste de datos por Kernels
    """
    def __init__(self, d, sigma):
        """  
        d: csv con "nuevos_casos" y "fecha_actualizacion"
        sigma = sigma de las gaussianas
        """
        self.d = d
        self.s = sigma
        try:
            1/self.s
        except ZeroDivisionError:
            print('Desviacion no puede ser 0, no se dará ajuste')

    def Dataframe(self):
        """ 
        Formatea y extrae información de un archivo .csv con columnas Nuevos_casos y Fecha_actualizacion 
        """
        self.df = pd.read_csv(self.d) 
        self.df.columns = self.df.columns.str.lower()
        self.y = self.df['nuevos_casos']                    
        self.y = (self.y)/(self.y).max()                                                                               # Normalizando
        self.df['fecha_actualizacion'] = pd.to_datetime(self.df['fecha_actualizacion'], format='%Y/%m/%d %H:%M:%S%z')  # Cambiando a formato datetime
        self.x = self.df['fecha_actualizacion']                                                                        # Fecha en formato necesario

        self.C = abs(self.x[0]-self.x)                                                                                 # Para gráficos
        for i in range(len(self.C)):
            self.C[i]=self.C[i].days

    def Kernel(self):
        """ 
        Se actualizan los datos para las gráficas, es un método interno para otros métodos
        """
        self.Dataframe()

        self.A = np.zeros((len(self.x),len(self.x)))
        self.B = np.zeros(len(self.x)) 

        self.C = abs(self.x[0]-self.x)                                                  # Arreglo de dias, solo para graficos
        for i in range(len(self.C)):
            self.C[i]=self.C[i].days

        self.D=[]

        for j in range(len(self.x)):
            for i in range(len(self.x)):
                self.A[j,i] = ((self.x[j]-self.x[i]).days)**2                           # .days Arreglo 2d con las diferencias de fechas al cuadrado

        for i in range(len(self.x)):
            self.D.append(self.y * np.exp(-self.A[i]/(2*self.s)))                       # Gaussianas para verificar el proceso sea exitoso (lo es)                  
            self.B[i]=self.D[i].sum()                                                   # .sum()    Ya para generar la curva suave    

    def Graph(self):
        """ 
        Grafica el arreglo original y el suavizado
        """
        self.Kernel()
        plt.plot(self.C, self.B/self.B.max(), color='red')
        #plt.plot(self.C, self.y)
        plt.xlabel('Días transcurridos desde primer caso')
        plt.ylabel('# Casos Nuevos / # Máximo de casos')
        plt.title('Covid 19 en Colombia')
        plt.show()

    def Derivada(self):
        """ 
        Da una gráfica de la derivada de la función original
        """
        self.Kernel()
        self.DB=np.zeros(len(self.C))
        for i in np.arange(1,len(self.C)):
            self.DB[i] =(self.B[i]-self.B[i-1])/(self.C[i]-self.C[i-1])
        plt.plot(self.C, self.DB)
        plt.xlabel('Días transcurridos desde primer caso')
        plt.title('Taza de Cambio de infectados')
        plt.show()