class Aluno:
    def __init__(self, nome, nota):
        self.nome = nome
        self.nota = nota

    def situacao(self):
        if self.nota >= 7:
            return f"{self.nome} está Aprovado"
        else:
            return f"{self.nome} está Reprovado com nota {self.nota}"

aluno1 = Aluno("Maria", 8.5)
aluno2 = Aluno("João", 5.0)

print(aluno1.situacao())
print(aluno2.situacao())