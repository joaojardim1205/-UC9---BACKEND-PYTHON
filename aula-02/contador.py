class Contador:
    def __init__(self):
        self.valor = 0

    def incrementar(self):
        self.valor += 1

    def mostrar(self):
        return self.valor

contador1 = Contador()
contador2 = Contador()

contador1.incrementar()
contador1.incrementar()
contador1.incrementar()

contador2.incrementar()

print(f"Contador 1: {contador1.mostrar()}")
print(f"Contador 2: {contador2.mostrar()}")