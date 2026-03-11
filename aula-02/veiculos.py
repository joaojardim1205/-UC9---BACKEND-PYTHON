class Veiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def ligar(self):
        return f"{self.marca} {self.modelo} está ligado!"


class VeiculoEletrico(Veiculo):
    def __init__(self, marca, modelo, autonomia):
        super().__init__(marca, modelo)
        self.autonomia = autonomia

    def carregar_bateria(self):
        self.autonomia = 400 
        return f"Bateria carregada! Autonomia: {self.autonomia} km"

    def ligar(self):
        return f"{self.marca} {self.modelo} está ligado! Autonomia restante: {self.autonomia} km"

carro_comum = Veiculo("Toyota", "Corolla")
carro_eletrico = VeiculoEletrico("Tesla", "Model 3", 300)

print(carro_comum.ligar())
print(carro_eletrico.ligar())
carro_eletrico.autonomia = 50
print(carro_eletrico.ligar())
print(carro_eletrico.carregar_bateria())