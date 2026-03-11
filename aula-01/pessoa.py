class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    def __str__(self):
        """Representação amigavel do objeto"""
        return f"{self.nome} | {self.idade} anos"
    
    def __len__(self):
        """Retorna da idade (conportamento personalizado)"""
        return self.idade

    def __repr__(self):
        """Representação para debug"""
        return f"Pessoa(nome='{self.nome}', idade={self.idade})"

p = Pessoa("Mariana", 25)
print(p)
print(str(p))
print(len(p))
print(repr(p))