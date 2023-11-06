import numpy as np
import inspect
import sympy as smp
import matplotlib.pyplot as plt

class mcInt:
    def __init__(self,f,a,b,N):
        """
        f: función a integrar
        a: límite inferior
        b: límite superior
        N: número de iteraciones

        Clase que calcula la integral de una función f en el intervalo [a,b]
        por el método de montecarlo y compara con la solución analítica.
        """

        self.f=f
        self.a=a
        self.b=b
        self.N=N

    def x_(self, iteraciones=None):
        """
        Devuelve un array random de x en el intervalo [a,b]
        """

        if iteraciones is None:
            iteraciones = self.N

        x_=np.random.uniform(self.a,self.b,iteraciones)
        return x_

    def Fstring(self):
        """
        Devuelve la función f en forma de string para poder usarla con sympy
        """

        f_lambda=inspect.getsource(self.f)
        sf_string=f_lambda.split(":")[1].strip()
        sf_string=sf_string.replace("y","y(x)")
        sf_string=sf_string.replace("np.","")
        
        return sf_string
    
    def analitica(self):
        """
        Devuelve la solución analítica de la integral de f en [a,b],
        y la función f evaluada en todo el array x
        """

        x=smp.Symbol('x')
        F=smp.sympify(self.Fstring()) #Convierte el string a una función de sympy
        return smp.integrate(F,(x,self.a,self.b)), smp.lambdify(x, F,"numpy")(self.x_())

    def yl(self):
        """
        Devuelve el máximo y mínimo de la función f en el intervalo [a,b]
        """
        efe =self.f(np.linspace(self.a,self.b))
        return max(efe),min(efe)
    
    def mcAreas(self,iteraciones=None):
        """
        Solución a la integral por montecarlo.
        """
        if iteraciones==None:
            iteraciones=self.N

        delta = (self.b-self.a)/iteraciones
        A = np.sum(self.f(self.x_()))*delta
        return A

    def plot(self, name : str = 'plotIntegral'):
        """
        Grafica la solución analítica y la solución por montecarlo.
        """

        print('\nGraficando')
        N_=range(1,self.N,self.N//10)
        S=np.zeros(len(N_))

        for i in range(len(N_)):
            S[i]=self.mcAreas(N_[i])
        plt.plot(N_,S,'.-',label='Montecarlo')
        plt.plot(N_,[self.analitica()[0]]*len(N_),label='Analítica')
        plt.title('Convergencia de la solución por método Montecarlo')
        plt.xlabel('Número de iteraciones')
        plt.grid()
        plt.legend()
        plt.savefig(name)
        return f'{name}.png'