import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class suavizado_gaussiano:

    def kernel(self, x, x0, sigma):
        try:
            return np.exp(-((x - x0) ** 2) / (2 * sigma ** 2)) / (sigma * (2 * np.pi)**(0.5))

        except:
            print("Ha ocurrido un error, verifique los valores")
        
    def suavizado_kernel(self, data, sigma=1): 

        try:
            datos_suavizados = np.zeros_like(data)

            for i in range(len(data)):
                peso = self.kernel(np.arange(len(data)), i, sigma)
                datos_suavizados[i] = np.sum(data * peso) / np.sum(peso)

            return datos_suavizados
        
        except:
            print("Error, intente volver a correr el programa con los elementos apropiados")
    
    def cargar_datos(self):

        try:

            self.data = pd.read_csv('datos_covid.csv')  # Reemplaza 'tus_datos.csv' con tu propio archivo CSV
            self.fecha_actualizacion = self.data['FECHA_ACTUALIZACION']
            self.fecha_actualizacion=np.array([self.fecha_actualizacion[i][0:10] for i in range(len(self.fecha_actualizacion))])
            self.nuevos_casos = self.data['NUEVOS_CASOS']

        except:

            print("Recuerde que debe cargar debidamente los archivos necesarios para ejecutar el programa.\
                Hay un error")

    def plot(self):

        try:

            self.cargar_datos()
            suavizado_nuevos_casos = self.suavizado_kernel(self.nuevos_casos, sigma=2)

            n = len(self.fecha_actualizacion)
            show_every_n = 50  
            indices = np.arange(0, n, show_every_n)
            show_dates = self.fecha_actualizacion[indices]

            plt.figure(figsize=(10, 6))
            plt.plot(self.fecha_actualizacion, self.nuevos_casos,label="Datos", marker='o', linestyle='', color='b',alpha=0.4)
            plt.plot(self.fecha_actualizacion, suavizado_nuevos_casos, label="suavizado kernel gaussiano", color='r', linewidth=2)
            plt.legend()
            plt.title('Casos nuevos de COVID-19')
            plt.xlabel('Fecha de actualización')
            plt.ylabel('Número de nuevos casos')
            plt.xticks(rotation=45)
            plt.xticks(indices, show_dates, fontsize=8)
            plt.tight_layout()
            plt.savefig('Casos nuevos Covid')
        
        except:
            print("Hubo un error al graficar, verifique los datos del archivo .csv")