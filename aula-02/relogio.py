
class Relogio:
    def __init__(self):
        self.hora = 0
        self.minuto = 0
        self.segundo = 0

    def ajustar_hora(self, h, m, s):
        if 0 <= h <= 23:
            self.hora = h
        else:
            print("Hora invalida! Use valores entre 0 e 23.")
            return

        if 0 <= m <= 59:
            self.minuto = m
        else:
            print("Minuto invalido! Use valores entre 0 e 59.")
            return

        if 0 <= s <= 59:
            self.segundo = s
        else:
            print("Segundo invalido! Use valores entre 0 e 59.")
            return

    def avancar_segundo(self):
        self.segundo += 1

        if self.segundo == 60:
            self.segundo = 0
            self.minuto += 1

        if self.minuto == 60:
            self.minuto = 0
            self.hora += 1

        if self.hora == 24:
            self.hora = 0

    def mostrar(self):
        return f"{str(self.hora).zfill(2)}:{str(self.minuto).zfill(2)}:{str(self.segundo).zfill(2)}"


relogio = Relogio()
relogio.ajustar_hora(23, 59, 58)

print(f"Hora inicial:  {relogio.mostrar()}")
relogio.avancar_segundo()
print(f"Após 1 segundo: {relogio.mostrar()}")
relogio.avancar_segundo()
print(f"Após 2 segundos: {relogio.mostrar()}")