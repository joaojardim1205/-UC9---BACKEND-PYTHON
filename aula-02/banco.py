class Banco:
    taxa_juros = 0.05

    def __init__(self, cliente, saldo):
        self.cliente = cliente 
        self.saldo = saldo

    def render_juros(self):
        juros = self.saldo * Banco.taxa_juros
        self.saldo += juros
        return f"{self.cliente}: saldo atualizado para R$ {self.saldo:.2f}"


conta1 = Banco("Maria", 1000)
conta2 = Banco("João", 5000)

print(f"Taxa atual: {Banco.taxa_juros * 100}%")
print(conta1.render_juros())
print(conta2.render_juros())

Banco.taxa_juros = 0.10
conta3 = Banco("Lúcia", 2000)
print(f"\nTaxa alterada para: {Banco.taxa_juros * 100}%")
print(conta3.render_juros())