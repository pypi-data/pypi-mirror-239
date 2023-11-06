import numpy as np
class Integrales:
    """ 
    """
    def __init__(self, a, b, f):
        """ 
        a: Inicio de intervalo de evaluacion
        b: Final de intervalo de evaluacion
        f: Funcion
        """
        self.a = a
        self.b = b
        self.f = f

    def Integrate(self):
        
        sum = 0
        for i in range(self.n):
            x = np.random.uniform(self.a,self.b)
            sum += (self.f(x))

        return ((self.b-self.a)/self.n)*sum    