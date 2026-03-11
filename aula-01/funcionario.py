class Funcionario:
    aumento = 1.05

    def __init__(self, nome, salario) -> None:
        self.nome = nome
        self.salario = salario

    def aplicar_aumento(self):
        self.salario *= Funcionario.aumento
        return f"Novo salario de {self.nome}: R$ {self.salario:.2f}"

func = Funcionario("Carlos", 2000)

print(f"Atributo de Classe: {Funcionario.aumento}")
print(f"Atributo via Instancia: {func.aumento}")
print(func.aplicar_aumento())
