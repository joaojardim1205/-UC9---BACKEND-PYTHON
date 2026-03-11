class ContaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.__saldo = saldo_inicial # atributo privado __saldo

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return f"Deposito de R$ {valor:.2f} realizado. Novo saldo R$ {self.__saldo}"
        return "valor invalido para deposito"

    def sacar(self, valor):
        if 0 < valor <= self.__saldo:
            self.__saldo -= valor
            return f"Saque de R$ {valor:.2f} realizado. Novo saldo R$ {self.__saldo}"
        elif valor > self.__saldo:
            return "Saldo insuficiente!"
        return f"Valor invalido para saque"

    def ver_saldo(self):
        return f"Saldo de {self.titular}: R$ {self.__saldo:.2f}"

conta = ContaBancaria("Ana", 1000)
print(conta.ver_saldo())
print(conta.depositar(500))
print(conta.sacar(200))
print(conta.depositar(1500))
print(conta.sacar(2000))
