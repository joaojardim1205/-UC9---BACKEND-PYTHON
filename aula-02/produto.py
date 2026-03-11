class Produto:
    contador_codigo = 0

    def __init__(self, nome, preco, categoria):
        if preco <= 0:
            raise ValueError(f"O preço deve ser positivo!")

        self.nome = nome
        self.preco = preco
        self.categoria = categoria
        Produto.contador_codigo += 1
        self.codigo = Produto.contador_codigo

    def aplicar_desconto(self, percentual):
        if percentual <= 0 or percentual >= 100:
            print("Percentual inválido! Use valores entre 0 e 100.")
            return
        desconto = self.preco * (percentual / 100)
        self.preco -= desconto
        return f"Desconto de {percentual}% aplicado. Novo preço: R$ {self.preco:.2f}"

produto1 = Produto("Notebook", 3500.00, "Eletronicos")
produto2 = Produto("Cadeira", 850.00, "Moveis")
produto3 = Produto("Mouse", 120.00, "Eletronicos")

print(f"Codigo: {produto1.codigo} | {produto1.nome} - R$ {produto1.preco:.2f}")
print(f"Codigo: {produto2.codigo} | {produto2.nome} - R$ {produto2.preco:.2f}")
print(f"Codigo: {produto3.codigo} | {produto3.nome} - R$ {produto3.preco:.2f}")

print(produto1.aplicar_desconto(10))

try:
    produto_invalido = Produto("Teste", -50, "Erro")
except ValueError as e:
    print(f"Erro: {e}")