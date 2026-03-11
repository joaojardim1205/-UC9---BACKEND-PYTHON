class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        print(f"Produto '{nome}' cadastrado!")

    def valor_total(self):
        total = self.preco * self.quantidade
        return f"Valor total no estoque de {self.nome}: R$ {total:.2f}"

    def vender(self, qtd):
        if qtd <= self.quantidade:
            self.quantidade -= qtd
            return f"Vendidos {qtd} unidades. Restam {self.quantidade}"
        else:
            return "Quantidade insuficiente!"
        
calcular = Produto("Celular", 1500, 10)
print(calcular.valor_total())
print(calcular.vender(3))