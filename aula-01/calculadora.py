class Calculadora:
    def saudacao(self):
        return "Ola, sou uma calculadora"

    def somar(self, a, b):
        resultado = a + b
        return f"{a} + {b} = {resultado}"

    def multiplicar(self, a, b):
        return f"{a} * {b} = {a*b}"

calc = Calculadora()
print(calc.saudacao())
print(calc.somar(10, 5))
print(calc.multiplicar(4, 3))