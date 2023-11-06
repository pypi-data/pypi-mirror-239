import numpy as np
import random
import sys
import matplotlib.pyplot as plt
from scipy import integrate


class mc_integ:
    """
    clase para solucionar la integral definida de una funcion usando metodo de MC.

    funcion: Funcion que se quiere integrar.
    inicio: Punto inicial en el que se quiere evaluar la funcion.
    final: Punto final en el que se quiere evaluar la funcion.
    numPasos: Numero de veces que se quiere correr el método.
    """

    def __init__(self, funcion, inicio, final, numPasos):
        self.f = funcion
        self.a = inicio
        self.b = final
        self.n = numPasos

    def errores(self):
        #reconocimiento de errores

        try:
            self.f(1)
        except:
            print('No ha ingresado una función válida')
            sys.exit(1)

        try:
            self.a / 2
        except:
            print('Ingrese un valor inicial válido.')
            sys.exit(1)

        try:
            self.b / 2
        except:
            print('Ingrese un valor final válido.')
            sys.exit(1)

        try:
            1 / (abs(self.n) + self.n)
        except:
            print('Ingrese un entero mayor a cero para el numero de pasos.')
            sys.exit(1)



    def MC(self):
        #Nos aseguramos que las variables sean válidas
        self.errores()

        #Calculamos la integral con montecarlo
        #Sacamos un resultado por cada uno de los componentes de x
        x = [random.uniform(self.a, self.b) for _ in range(self.n)]
        fun = np.zeros(len(x))
        for i in range(len(x)):
            fun[i] = self.f(x[i])
        I = (self.b - self.a) / self.n * sum(fun)
        return I, fun, x

    
    def solucionExacta(self):
        #Nos aseguramos que las variables sean válidas
        self.errores()
        
        #Hacemos una lista con las integrales definidas dentro del intervalo
        array = np.linspace(self.a, self.b, self.n)
        int = [integrate.quad(self.f, self.a, i)[0] for i in array]
        
        return array, int

    
    def figPlot(self):
        #Nos aseguramos que las variables sean válidas
        self.errores()
        
        #graficamos ambos metodos de integracion
        plt.scatter(self.MC()[2], self.MC()[1], label = 'Puntos para Monte Carlo')
        plt.plot(self.solucionExacta()[0], self.solucionExacta()[1], 'r-', label = 'Solucion Exacta')
        plt.plot(self.solucionExacta()[0][-1], self.MC()[0], 'ko', label = 'Solucion')
        plt.title('Resultado = {}, n de Iter = {}'.format(self.MC()[0], self.n))
        plt.legend()
        plt.savefig('Soluciones_Integral')



        