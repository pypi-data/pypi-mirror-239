import numpy as np

class aritmetica:
    """
    Esta calse suma
    """
    
    def __init__(self,a,b):
        """
        Esta funcion inicializa la clase suma
        """
        self.a = a
        self.b = b
        
    def suma(self):
        """
        Esta funcion suma dos numeros
        """
        return self.a + self.b
    
    def resta(self):
        """
        Esta funcion resta dos numeros
        """
        return self.a - self.b
    
    def multiplicacion(self):
        """
        Esta funcion multiplica dos numeros
        """
        return self.a * self.b
    
    def division(self):
        """
        Esta funcion divide dos numeros
        """
        return self.a / self.b
    
    def potencia(self):
        """
        Esta funcion eleva a la potencia dos numeros
        """
        return self.a ** self.b
    
    def raiz(self):
        """
        Esta funcion calcula la raiz cuadrada de un numero
        """
        return np.sqrt(self.a) , np.sqrt(self.b)
