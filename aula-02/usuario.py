class Usuario:
    def __init__(self, nome, email, idade):
        self.nome = nome
        self.email = email
        self.idade = idade

    def anos_para_aposentadoria(self):
        aposentadoria = 65
        anos_restantes = aposentadoria - self.idade
        if anos_restantes <= 0:
            return f"{self.nome} já pode se aposentar!"
        return f"{self.nome} ainda tem {anos_restantes} anos para se aposentar."

usuario1 = Usuario("Ana", "ana@email.com", 30)
usuario2 = Usuario("Carlos", "carlos@email.com", 60)

print(usuario1.anos_para_aposentadoria())
print(usuario2.anos_para_aposentadoria())