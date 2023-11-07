import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class suavizado:

    def __init__(self, nombreDocumento, sigma):
        self.df = pd.read_csv(nombreDocumento)
        self.sigma = sigma

    def kerGaus(self, numCasos, sigma):
        def func(x, x_, sigma):
            return np.exp(-(abs(x-x_)) ** 2 / (2*sigma))
        datos_f = np.zeros_like(numCasos)

        for i in range(len(numCasos)):
            pesos = func(np.arange(len(numCasos)), i, sigma)
            datos_f[i] = np.sum(numCasos * pesos)/ np.sum(pesos)

        return datos_f
    
    def figPlot(self):
        y = self.kerGaus(self.df.NUEVOS_CASOS, 50)

        places = np.linspace(0, len(self.df) - 1, 8)
        ticks = []

        for i in places:
            ticks.append(self.df.FECHA_ACTUALIZACION[int(i)].split(' ')[0])


        plt.plot(self.df.FECHA_ACTUALIZACION, self.df.NUEVOS_CASOS)
        plt.plot(self.df.FECHA_ACTUALIZACION, y)
        plt.xticks(places, ticks, rotation = 45)
        plt.ylabel('Nuevos casos')
        plt.savefig('Nuevos_Casos_Suavizado.png')