import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt

class MonteCarloIntegration:
    def __init__(self, func, a, b):
        self.func = func
        self.a = a
        self.b = b

    def calculate_exact_integral(self):
        inte=integrate.quad(self.func, self.a, self.b)
        return inte

    def calculate_monte_carlo_integral(self,n):
        if n<=0:
            raise ValueError("El número de iteraciones debe ser mayor a cero")
        
        x_values = np.random.uniform(self.a, self.b, n)
        y_values = self.func(x_values)
        integral = (self.b - self.a) * np.mean(y_values)
        print(f"La integral aproximada con el método Monte Carlo es: {integral}")
    
    def calculate_monte_carlo_integralint(self,n):
        if n<=0:
            raise ValueError("El número de iteraciones debe ser mayor a cero")
        
        x_values = np.random.uniform(self.a, self.b, n)
        y_values = self.func(x_values)
        integral = (self.b - self.a) * np.mean(y_values)
        return integral
    
    def figplot(self,n):
        exact_integral = self.calculate_exact_integral()
        print(f"La integral exacta es: {exact_integral[0]}")
        app=np.zeros(n)
        for i in range(1,n):
            self.integral=self.calculate_monte_carlo_integralint(i)
            app[i]=self.integral
        plt.figure(figsize=(10,5))
        plt.plot(app,"blue",label="Montecarlo")
        plt.plot([exact_integral[0] for i in range(n)],"red",label="Solución analítica")
        plt.legend()
        plt.grid()
        plt.xlabel("Número de iteraciones")
        plt.show()