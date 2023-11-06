import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class GaussianKernel:
    def __init__(self,data,sigma):
        self.sigma=sigma
        self.data=data

    def gaussian_kernel_smoother(self):
        nuevos_casos=self.data['NUEVOS_CASOS']
        smoothed_data = np.zeros_like(nuevos_casos)
        n = len(nuevos_casos)

        for i in range(n):
            weights=np.exp(-((np.arange(n) - i) ** 2) / (2 * self.sigma ** 2)) / (np.sqrt(2 * np.pi) * self.sigma)
            smoothed_data[i] = np.sum(nuevos_casos * weights) / np.sum(weights)

        return smoothed_data    
        
    def plot(self):
        fecha_actualizacion = self.data['FECHA_ACTUALIZACION']
        fecha_actualizacion=np.array([fecha_actualizacion[i][0:10] for i in range(len(fecha_actualizacion))])
        nuevos_casos=self.data['NUEVOS_CASOS']
        smoothed_nuevos_casos=self.gaussian_kernel_smoother()

        n = len(fecha_actualizacion)
        show_every_n = 50  
        indices = np.arange(0, n, show_every_n)
        show_dates = fecha_actualizacion[indices]

        plt.figure(figsize=(10, 6))
        plt.plot(fecha_actualizacion, nuevos_casos,label="Datos",markersize=5, marker='o', linestyle='', color='b',alpha=0.5)
        plt.plot(fecha_actualizacion, smoothed_nuevos_casos, label="Gaussian kernel smoother", color='r', linewidth=2)
        plt.legend()
        plt.title('Casos nuevos de COVID-19')
        plt.xlabel('Fecha de actualización')
        plt.ylabel('Número de nuevos casos')
        plt.xticks(rotation=45)
        plt.xticks(indices, show_dates, fontsize=8)
        plt.tight_layout()
        plt.show()