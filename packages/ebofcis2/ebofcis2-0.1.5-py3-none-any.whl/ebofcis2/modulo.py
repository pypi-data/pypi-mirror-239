import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tqdm
import sympy as sp


class ajuste_curva:

    """
    
    Clase que nos va a permitir por medio de un kernel gaussiano
    suavisar la curva de unos datos, en este caso, datos realacionados
    con los nuevos casos de COVID-19 por días.
    
    """

    def __init__(self, path):
        
        """
        Constructor de la clase.
        Recibe la dirección del archivo csv con los datos.
        ¡¡ El csv debe tener las siguientes columnas!! 
        -- 'fecha_actualizacion' : fecha de actualización de los datos
        -- 'nuevos_casos'  : número de casos nuevos en el día
        """

        self.path = path
        usecols = ['FECHA_ACTUALIZACION', 'NUEVOS_CASOS']
        try:
            self.data = pd.read_csv(self.path, sep=',', header=0, usecols=usecols)
        except Exception as e:
            print(f'Error al leer el archivo, revise la dirección y/o estructura del archivo{e}') 
            self.data = None
        self.x = np.arange(0, len(self.data['FECHA_ACTUALIZACION']),1)
        self.y = self.data['NUEVOS_CASOS'].to_numpy()

    def kernel_gauss(self, x_a, x, r):
            
        """
        Método que nos permite calcular el kernel gaussiano.
        Recibe:
        -> x_a: punto al que se quiere evaluar
        -> x: punto en el que se encuentra
        -> r: valor de r para determinar sigma

        """    
        try:
            sigma = 1/r
            w = 1 # Factor de normalización
            k = w * np.exp(-np.abs(x_a-x)**2/(2*sigma))
        except Exception as e:
            print(f'Error al calcular el kernel gaussiano{e}')
        else:
            return k

    def curva(self,x,y,r):
        """
        Método que nos permite calcular la curva suavizada.
        Recibe:
        -> x: datos en x (cantidad de días)
        -> y: datos en y (nuevos casos)
        -> r: valor de r para determinar sigma

        return: curva suavizada
        """

        try:
            
            y = np.zeros(len(self.x))
            for j in tqdm.tqdm(range(len(self.x))):
                y_i= []
                for i in range(len(self.x)):
                    y_i.append(self.kernel_gauss(self.x[j],self.x[i],r)*self.y[i])
                    # print(y_i[i])
                y[j] = np.sum(y_i)

            return (self.y.max()*y)/y.max()
                    
        except Exception as e:
            print(f"Error al calcular la curva suavizada{e}")




    def plot(self):
        
        """
        Método que nos permite graficar los datos vs la curva suavizada.
        """

        try:
            y = self.curva(self.x,self.y,0.1)
            plt.plot(self.x, self.y,label='Datos')
            plt.plot(self.x, y,label='Curva suavizada')
            plt.legend()
        except Exception as e:
            print(f"Error al graficar los datos{e}")
        else:
            plt.savefig('data.png')    


class Integral_montecarlo:

    """ Clase para calcular integrales por el metodo de montecarlo  """

    def __init__(self, f, a, b, n):
        
        """ Método constructor de la clase Integral_montecarlo
        :param f: Función a integrar en formato sympy
        :param a: Limite inferior de integración
        :param b: Limite superior de integración
        :param n: Número de interaciones  """

        self.f = f
        self.a = a
        self.b = b
        self.n = n
        x = sp.Symbol('x')
        self.f1 = sp.lambdify('x', self.f(x), 'numpy')
        self.integrada = sp.lambdify('x', self.f(x), "numpy")
        
        
    def x_monte(self,x):
            
            """ Método para generar los valores aleatorios en el intervalo [a,b]
            :param x: Número de iteraciones (Tamaño del intervalo)
            :return: Valores aleatorios en el intervalo [a,b] con tamaño x """
            try:
                xm = np.random.uniform(self.a, self.b, x)
            except:
                print("No se puede generar el vector de aleatorios")
            else:
                return xm        

    def area(self,x):

        """ Método para calcular el valor de la integral por el metodo de montecarlo 
        :param x: Número a evaluar en la función 
        :return: Valor de la integral por el método de montecarlo"""

        
        try:
            area = (self.b - self.a ) * np.mean(self.f1(self.x_monte(x)))
        except Exception as e:
            print("No se puede calcular el valor de la integral",e)
        else:
            return area
    
    def analitica(self):
        
        """ Método para calcular el valor de la integral por el metodo analítico"""
        try :
            x = sp.Symbol('x')
            f = sp.integrate(self.f(x), (x, self.a, self.b))
        except Exception as e:
            print("No se puede calcular el valor de la integral",e)
        else:
            return f
    
    
    def plot(self):
        
        """ Método para graficar la solución analítica y la 
        solución por el método de montecarlo 
        :return: Plot de la solución analítica vs la solución por
          el método de montecarlo """
        
        try:
            print('Graficando...')
            x = self.x_monte(self.n)
            x = np.sort(x)
            y_analitica   = []
            y_monte = []
            
            for i in x:
                y_monte.append(self.area(self.n))
                y_analitica.append(self.integrada(i))
        except Exception as e:
            print("No se pudo realizar el plot",e)
        else:
            plt.title('Integral por método de Montecarlo vs analítica')
            plt.plot(x,y_analitica, label = 'Analítica')
            plt.plot(x,y_monte,'.', label = 'Montecarlo')
            plt.grid()
            plt.legend()

            plt.savefig('montecarlo.png') 
            plt.close()
            print('Grafica guardada en montecarlo.png')
            
            return True
    
    def plot_iteraciones(self,n,N):

        """ Método para mirar como va convergiendo el método de montecarlo 
        :param n: paso para el número de iteraciones 
        :param N: número de iteraciones 
        :return: Plot de la convergencia del método de montecarlo"""

        try:
            print('Graficando...')
            
            monte = []
            analitica = []
            for i in range(1,N,n):
                monte.append(self.area(i))
                analitica.append(self.analitica())
        except Exception as e:
            print("No se pudo realizar el plot de montecarlo vs analitica",e)
        else:
            plt.title('Iteraciones del método de Montecarlo')
            plt.plot(monte, label = 'Montecarlo')
            plt.plot(analitica, label = 'Analítica')
            plt.legend()    
            plt.xlabel('Iteraciones')
            plt.ylabel('Valor de la integral')
            plt.grid()
            plt.savefig('iteracion.png')
            plt.close()
            print('Grafica guardada en iteracion.png')
            return True