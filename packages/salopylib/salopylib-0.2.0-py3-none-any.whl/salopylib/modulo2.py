import numpy as np
import matplotlib.pyplot as plt
import sympy as sy 
import inspect
class integralMC:

    """
    Esta clase realiza la integración definida de una función en un intervalo con el método de montecarlo y compara su valor con el analítico
    Se deben ingresar los parámteros:
    funcion: funcion f(x) a integrar. debe definirse con un lambda.
    xmin, xmax: intervalo sobre el cual se realiza la integración
    niter: número de iteraciones con las que se implementa montecarlo. Debe ser un array para comparar los valores de la integral
        en función del número de iteraciones

    Y contiene los siguientes métodos:
    intf: realiza la integración con montecarlo. devuelve el valor de la integral para cada niter
    Fstring: convierte una función definida con lambda en un string para poder integrarla usando la librería de sympy
    ana_int: calcula el valor de la integral de forma analítica
    plot_int: grafica el valor de la integral con montecarlo vs número de iteraciones usadas y compara cada punto con el valor real
    """

    def __init__(self,funcion,xmin:float,xmax:float,niter:int): #atributos
        self.f = funcion
        self.a = xmin
        self.b = xmax
        self.n = niter
        
    def intf(self):
        try:
            N = len(self.n)
            sf = np.zeros(N)
            for i in range(N):
                dx = (self.b-self.a)/self.n[i]
                xi = np.random.uniform(self.a,self.b,self.n[i])
                sf[i] = np.sum(self.f(xi))*dx
            return sf
        except:
            print('Ingrese un arreglo para niter')

    def Fstring(self):
        try:
            f_lambda=inspect.getsource(self.f)
            sf_string=f_lambda.split(":")[1].strip()
            #sf_string=sf_string.replace("y","y(x)")
            sf_string=sf_string.replace("np.","")
            return sf_string
        except:
            print('Ingrese una funcion valida')

    def ana_int(self):
        try:
            x = sy.Symbol('x')
            f=sy.sympify(self.Fstring())
            return sy.integrate(f,(x,self.a,self.b))
        except:
            pass
    
    def plot_int(self):
        try: 
            plt.figure(figsize=(8,8))
            plt.grid()
            plt.xlabel('numero de iteraciones')
            plt.ylabel('Valor de la integral')
            plt.title('Comparacion del resultado')
            plt.plot(self.n,self.intf(),'-o',c='deeppink',label='con Montecarlo') 
            plt.axhline(y=self.ana_int(),c='m',label='Analiticamente')
            plt.legend()
            plt.savefig('grafica_integral.png')
            plt.show()   
        except:
            pass  
