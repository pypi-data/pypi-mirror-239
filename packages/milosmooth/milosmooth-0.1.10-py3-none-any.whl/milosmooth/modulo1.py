import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class smoother:
    """
    Esta clase lee un archivo csv con datos de casos nuevos de covid-19 en Colombia,
    con columnas ```casos``` y ```fechas```, y genera un ajuste 
    suave de los datos
    """
    def __init__(self, path : str , r : float, casos='nuevos_casos', fechas='fecha_actualizacion'):
        """
        path: direccion del archivo csv
        r: factor de suavizado (0<r<1, entre mas cercano a 0, mas suavizado)
        
        Esta clase lee un archivo csv con datos de casos nuevos de covid-19 en Colombia,
        con columnas ```casos``` y ```fechas```, y genera un ajuste 
        suave de los datos
        """

        self.doc = pd.read_csv(path)
        self.sg=1/r
        self.y=self.doc[casos]
        self.fechas=pd.to_datetime(self.doc[fechas])
        self.x=np.arange(0,len(self.y),1)

    def kerneli(self, x : float ,xi : float ,y : float):
        """
        x: vector de fechas
        xi: dato a evaluar
        y: vector de casos nuevos

        Este metodo calcula el kernel de la funcion de suavizado
        """

        kernel= lambda x,xi,y: y*np.exp(-abs(x-xi)**2/(2*self.sg))
        return kernel(x,xi,y)
    
    def kernelisum(self, X : float):
        """
        X: vector de fechas

        Este metodo calcula la suma de los kernels de la funcion de suavizado,
        dando el valor de la funcion de suavizado en X
        """

        kernelsum=0
        for i in range(len(self.x)):
            ks=self.kerneli(X,self.x[i],self.y[i])
            kernelsum+=ks
        return kernelsum
    
    def arraysum(self):
        """
        Este metodo calcula la funcion de suavizado en todo el rango de fechas
        """

        Y=np.zeros(len(self.x))
        for i in range(len(self.x)):
            Y[i]=self.kernelisum(self.x[i])
        maximo=max(Y)
        return max(self.y)*Y/maximo

    def plot(self, name : str = 'plotCovid'):
        """
        Este metodo grafica los datos y el ajuste suave y guarda la imagen
        """
        plt.figure()
        plt.plot(self.fechas,self.y,label='Datos')
        plt.plot(self.fechas,self.arraysum(),label='Ajuste')
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.savefig(name)
        plt.show()

        return f'{name}.png'
    
