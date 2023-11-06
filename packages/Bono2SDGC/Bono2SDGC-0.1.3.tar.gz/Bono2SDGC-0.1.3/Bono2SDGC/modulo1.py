import numpy as np
class Integrales:
    """ 
    """
    def __init__(self, a, b, n, f):
        """ 
        a: Inicio de intervalo de evaluacion
        b: Final de intervalo de evaluacion
        n: Numero de generaciones arbitrarias en el rango
        f: Funcion
        """
        self.a = a
        self.b = b
        self.f = f
        self.n = n

    def Integrate(self):
        
        sum = 0
        for i in np.arange(self.n):
            x = np.random.uniform(self.a,self.b)
            sum += (self.f(x))

        return ((self.b-self.a)/self.n)*sum    