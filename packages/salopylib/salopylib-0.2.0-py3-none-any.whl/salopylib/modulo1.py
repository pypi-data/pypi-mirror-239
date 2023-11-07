import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ajusteGauss:
    '''
    Clase que realiza el ajuste de datos de fecha vs cantidad a una curva suave por medio de un kernel 
    gaussiano y hace su respectiva graficación, a partir de los siguientes datos:
    path: direccción en que se encuentra el archivo csv que contiene los datos. 
    r: factor que determina la "suavidad" de la curva y la exactitud del ajuste. Entre menor sea su valor
        más suave será la curva de ajuste pero más se alejará de los datos ingresados y vicecversa.
    '''

    def __init__(self,path:str,r:float):
        self.p = path
        self.s = 1/r
    
    def datos(self):
        df = pd.read_csv(self.p)
        return df
    
    def ajuste(self):
        suavizado = []
        df = self.datos()
        df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])

        for f in sorted(df['fecha_actualizacion']):
            df['suave'] = np.exp(
                -(((df['fecha_actualizacion'] - f).apply(lambda x: x.days)) ** 2) / (2 * self.s)
            )
            df['suave'] /= df['suave'].sum()
            suavizado.append(round(df['nuevos_casos'] * df['suave']).sum())
        df['suavizado'] = suavizado

        return df

    def graph_aj(self):
        df = self.ajuste()
        plt.figure(figsize=(10, 6))
        plt.grid()
        plt.title('Casos de covid-19 en Colombia')
        plt.xlabel('Fechas [aaaamm]')
        plt.ylabel('Número de casos')
        plt.plot(df['fecha_actualizacion'], df['nuevos_casos'], label='Datos originales')
        plt.plot(df['fecha_actualizacion'], df['suavizado'], label='Curva suavizada')
        plt.legend()
        plt.show()

    
