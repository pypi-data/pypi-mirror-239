import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class KernelGaussiano(object):
    """
    Esta clase implementa el kernel gaussiano para suavizar una serie de tiempo.
    
    Parámetros:
    -----------
    data: str
        Ruta del archivo csv con los datos de la serie de tiempo.
    sigma: float
        Parámetro de suavizado.
        
    Métodos:
    --------
    PlotGaussianKernel()
        Grafica la serie de tiempo original y la suavizada.
    """
    
    
    def __init__(self,data,sigma):
        """
        Inicializa la clase KernelGaussiano.
        
        Parámetros:
        -----------
        data: str
            Ruta del archivo csv con los datos de la serie de tiempo.
            
        sigma: float
            Parámetro de suavizado.
        """
        self.sigma = sigma
        
        if not data.endswith('.csv'):
            raise ValueError("Data must be a .csv file")
        
        self.data  = pd.read_csv(data)
        
        if not isinstance(self.data,pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame")
        if not isinstance(self.sigma,(int,float)):
            raise TypeError("Sigma must be a number")
        if self.sigma <= 0:
            raise ValueError("Sigma must be positive")
        if 'nuevos_casos' not in self.data.columns.str.lower():
            raise ValueError("Data must have 'nuevos_casos' column")
        if 'fecha_actualizacion' not in self.data.columns.str.lower():
            raise ValueError("Data must have 'fecha_actualizacion' column")
    
    def PlotGaussianKernel(self):
        """
        Este método grafica la serie de tiempo original y la suavizada.
        La suaivización se realiza con el kernel gaussiano.
        
        Retorna:
        --------
        Gráfica de la serie de tiempo original y la suavizada.
        """
        
        
        #cargar datos
        df = self.data.copy()
        #convertimos columnas en minuscula  
        df.columns = df.columns.str.lower()
        #transformamos a formato de fecha 
        df['fecha_actualizacion'] = pd.to_datetime(df['fecha_actualizacion'])
        #separamos la fecha de la hora
        df['fecha_actualizacion'] = df['fecha_actualizacion'].dt.date
        
        #sacamos la columna de nuevos casos
        data = df['nuevos_casos'].to_numpy()
        
        # Algoritmo del suavizado con kernel gaussiano
        def gaussiankernel(data, sigma):
            gaussKernel = lambda x,x_,sigma: np.exp(-(abs(x-x_))**2/(2*sigma)) 
            smoothed_data = np.zeros_like(data)
            
            for i in range(len(data)):
                pesos = gaussKernel(np.arange(len(data)), i, sigma)
                smoothed_data[i] = np.sum(data * pesos)/np.sum(pesos)
                
            return smoothed_data
        
        #creamos una nueva columna con los datos suavizados
        df['casos'] = gaussiankernel(data, sigma=18/2)
        df = df.set_index('fecha_actualizacion')

        #graficamos
        _, ax = plt.subplots(figsize=(25,10))
        ax.plot(df['nuevos_casos'], 'ko', label='Data')
        ax.plot(df['casos'], 'r-', linewidth=3, label='Suavizado')
        ax.legend(fontsize=20)
        ax.tick_params(axis='both', labelsize=20)
        plt.xticks(rotation=90)
        ax.set_xlabel('Fecha', fontsize=20)
        ax.set_ylabel('Número de nuevos casos', fontsize=20)
        ax.set_title('Número de nuevos casos de COVID-19', fontsize=20)
        plt.show()

# if __name__ == "__main__":
#     data = "/home/luciano/FC120232/Bono 2/Colombia_COVID19_Coronavirus_casos_diarios.csv"
#     sigma = 18/2
#     kernel = GaussianKernel(data,sigma)
#     kernel.PlotGaussianKernel()
