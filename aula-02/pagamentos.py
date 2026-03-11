class Pagamento:
    def processar(self):
        return "Processando pagamento..."


class CartaoCredito(Pagamento):
    def __init__(self, numero_cartao, parcelas):
        self.numero_cartao = numero_cartao
        self.parcelas = parcelas

    def processar(self):
        return f"Pagamento no cartão de credito {self.numero_cartao} em {self.parcelas}x aprovado!"


class Boleto(Pagamento):
    def __init__(self, vencimento):
        self.vencimento = vencimento

    def processar(self):
        return f"Boleto gerado! Vencimento: {self.vencimento}. Pague em qualquer banco."


class Pix(Pagamento):
    def __init__(self, chave):
        self.chave = chave

    def processar(self):
        return f"Pix enviado para a chave: {self.chave}. Pagamento instantâneo!"


def finalizar_compra(pagamento):
    print("Finalizando compra...")
    print(pagamento.processar())
    print("Compra concluída!\n")

cartao = CartaoCredito("1234567890123456", 3)
boleto = Boleto("27/02/2026")
pix = Pix("pagamento@empresa.com")

finalizar_compra(cartao)
finalizar_compra(boleto)
finalizar_compra(pix)