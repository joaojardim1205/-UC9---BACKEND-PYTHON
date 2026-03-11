class Eletronico: # Classe pai
    def __init__(self, nome):
        self.nome = nome
        self.ligado = False

    def ligar(self):
        if not self.ligado:
            self.ligado = True
            return f"{self.nome} ligado!"
        return f"{self.ligado} já está ligado!"
    
    def desligar(self):
        if self.ligado:
            self.ligado = False
            return f"{self.nome} está desligado!"
        return f"{self.ligado} já está desligado!"

class Smartphone(Eletronico): # Classe  filha
    def tirar_foto(self):
        if self.ligado:
            return f"Foto tirada com o {self.nome}"
        else:
            return f"Ligue o {self.nome} primeiro!"

iphone = Smartphone("iPhone")
print(iphone.tirar_foto())
print(iphone.ligar())
print(iphone.tirar_foto())
print(iphone.desligar())