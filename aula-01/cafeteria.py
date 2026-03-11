class Cafeteria:
    def __init__(self, modelo):
        self.modelo = modelo
        self.agua_quente = False
        self.cafe_pronto = False

    # Metodo Publico
    def fazer_cafe(self):
        print(f"Preparando café na {self.modelo}...")
        self.__aquecer_agua()
        self.__moer_graos()
        self.__coar()
        self.cafe_pronto = True
        return "Café pronto! Bom apetite!"

    # Metodos Privados
    def __aquecer_agua(self):
        print("Aquecendo agua...")
        self.agua_quente = True

    def __moer_graos(self):
        print("Moendo grãos...")

    def _coar(self):
        if self.agua_quente:
            print("Coando o café...")
        else:
            print("Erro: Agua não está quente!")
    
    def __verificar_reservatorio(self):
        """Outro Metodo Privado"""
        return "Reservatorio OK"

# Usando a cafeteira
minha_cafeteira = Cafeteria("Expresso Premium")

# O usuario só precisa saber disso
print(minha_cafeteira.fazer_cafe())

# minha_cafeteira.__aquecer_agua() # Erro - MÉTODO PRIVADO NÂO INICIALIZA AQUI