import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np


class intMC(object):
    """
    Esta clase permite calcular integrales utilizando el método de Monte Carlo y comparar los resultados
    con el valor exacto. También proporciona una representación gráfica del valor de la integral calculada 
    con el método de Monte Carlo y el valor exacto en función del número de iteraciones.
    
    Parámetros:
    - f: funcion a integrar
    - a: limite inferior de la integral
    - b: limite superior de la integral
    - N: numero de puntos aleatorios

    Métodos:
    - IntegrateMC: calcula la integral por el metodo de Monte Carlo
    - IntegrateEx: calcula la integral exacta
    - PlotMC: Compara el valor numerico de la integral con el valor exacto y grafica el valor de la integral en funcion del numero de iteraciones
    
    """
    
    def __init__(self, f, a, b, N):
        """
        Inizializa los parametros de la clase
        
        ARGUMENTOS
        - f: funcion a integrar
        - a: limite inferior de la integral
        - b: limite superior de la integral
        - N: numero de puntos aleatorios
        """
        self.f = f
        self.a = a
        self.b = b
        self.N = N
        if not callable(self.f):
            raise ValueError("La funcion debe ser callable")
        if not isinstance(self.a, (int, float)):
            raise ValueError("El limite inferior debe ser un numero")
        if not isinstance(self.b, (int, float)):
            raise ValueError("El limite superior debe ser un numero")
        if not isinstance(self.N, int):
            raise ValueError("El numero de puntos debe ser un numero entero")
        if self.N <= 0:
            raise ValueError("El numero de puntos debe ser mayor que cero")
        if self.a > self.b or self.a == self.b:
            raise ValueError("El limite inferior debe ser menor que el limite superior")
        if not self.continuous():
            raise ValueError("La funcion debe ser continua en el intervalo [a,b]")
    
    def Continuous(self):
        """
        Este metodo verifica que la funcion sea continua en el intervalo [a,b]
        """
        x = np.linspace(self.a, self.b, self.N)
        is_continuous  = all(abs(self.f(x) - self.f(x + 1e-9)) < 1e-6 for x in x[:-1]) 
        #is_continuous = np.all(np.isfinite(self.f(x)))
        return is_continuous
    
    def IntegrateMC(self):
        """
        Esta funcion realiza la integral por el metodo de Monte Carlo
        
        Retorna:
        - I: valor numerico de la integral
        """
        try:
            # Genera N numeros aleatorios entre a y b
            x = np.random.uniform(self.a, self.b, self.N)
            
            # Evalua la funcion en los puntos aleatorios
            fx = self.f(x)
            # Calcula la integral
            I = ((self.b - self.a))* np.mean(fx)
            
        except Exception as e:
            raise ValueError("Cambie los parametros de la integral o la funcion a integrar")
    
    def IntegrateEx(self):
        """
        Esta funcion calcula la integral exacta
        
        retorna:
        - sol: valor exacto de la integral
        """
        try:
            sol = integrate.quad(self.f, self.a, self.b)
        except Exception as e:
            raise ValueError("Cambie los parametros de la integral o la funcion a integrar")
        
    def PlotMC(self):
        """
        Esta funcion grafica el valor de la integral en funcion del numero de iteraciones
        
        Retorna:
        - Grafica del valor de la integral calculada con el metodo de Monte Carlo y el valor exacto en funcion del numero de iteraciones
        """
        try:
            #Iteraciones
            x = [i for i in range(1,self.N,10)]
            
            #Valor numerico de la integral para cada iteracion
            valor_numerico = [(self.b - self.a) * np.mean(self.f(np.random.uniform(self.a, self.b, i))) \
                            for i in range(1,self.N,10)]
            
            #Valor exacto de la integral para cada iteracion
            valor_exacto = [self.integrateEx() for i in range(1,self.N,10)]
            
            #Grafica
            _ , ax = plt.subplots()
            ax.plot(x,valor_numerico,"k-",label="Valor de la integral con Monte Carlo") 
            #con linea mas delgada
            ax.plot(x,valor_exacto,"r-",label = "Valor analitico de la integral", linewidth=1)
            ax.set_xlabel("Iteraciones")
            ax.set_ylabel("Valor de la integral")
            ax.legend()
            ax.grid()        
            #guarda la grafica
            plt.savefig("intmontecarlo.png")
            plt.show()
            
        except Exception as e:
            raise ValueError("Cambie los parametros de la integral o la funcion a integrar")