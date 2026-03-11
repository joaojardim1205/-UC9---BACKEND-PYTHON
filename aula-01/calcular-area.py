import math

class Forma: # Classe pai
    def area(self):
        return 0
    
class Quadrado(Forma): # Classe filha
    def __init__(self, lado):
        self.lado = lado

    def area(self):
        return self.lado ** 2
    
class Circulo(Forma):
    def __init__(self, raio):
        self.raio = raio

    def area(self):
        return math.pi * self.raio ** 2
    
# Funcao polimorfica
def calcular_area(forma):
    nome = type(forma).__name__
    print(f"Area do {nome}: {forma.area():.2f}")

formas = { # Array
    Quadrado(5),
    Circulo(3),
    Quadrado(2),
    Circulo(4)
}

for forma in formas: # laço de repetição
     calcular_area(forma)