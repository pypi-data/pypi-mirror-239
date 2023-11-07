import scipy.integrate as integrate
import numpy as np
import matplotlib.pyplot as plt


class I_Montecarlo:
    
    '''
    aquesta clase resuelve la integral definida de una función en un intervalo dado (a,b).
    Se da solución con el método de monte carlo y posteriormente se compara con la solución
    analítica. 
    f : Función que se integra.
    n : Número de iteraciones
    a,b: Intervalo de integración
    
    '''

    
    def __init__(self, f, n, a, b):
      self.f = f
      self.n = n
      self.a = a
      self.b = b
       
        
    def I_analitica(self):
        resultado = integrate.quad(self.f,self.a,self.b) 
        return resultado[0]

    def montecarlo(self,h): 
        try:
            x_a = np.random.uniform(self.a, self.b,h)  
            f_v = np.vectorize(self.f)
            promedio=sum(f_v(x_a))/h
            return (self.b - self.a)*promedio
        except:
            print("Error al ejecutar el método de Monte Carlo. Revise los valores asignados \
                al objeto de la class I_Montecarlo")

        
    def plot(self):
        i_monte = []
        iteraciones = np.arange(1,self.n,1)

        for i in range(1,len(iteraciones)+1):
            i_monte.append(self.montecarlo(i))
                
        analitica = self.I_analitica()
            
        plt.plot(iteraciones, i_monte, label='Montecarlo')
        plt.hlines(analitica,0,self.n, color="red", label='Analítica')
        plt.title('Integral Analítica vs Método Montecarlo')
        plt.xlabel('Número de iteraciones')
        plt.ylabel('Resultado de la integral')
        plt.legend()
        plt.savefig('Analitica_vs_Montecarlo.png')

    def run(self):

        try:
            self.I_analitica()
        except ZeroDivisionError:
            print("Error al dividir por cero")

        try:
            self.plot()
        except ZeroDivisionError:
            print("Error al dividir por cero")

        try:
            self.I_analitica()
        except:
            print("Error. Verifique los valores")
        
        try:
            self.plot()
        except:
            print("Error. Verifique los valores")