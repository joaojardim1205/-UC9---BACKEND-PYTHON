class Livro: # Nome da classe
    def __init__(self, titulo): # Atributo
        self.titulo = titulo

    def ler(self): # Metodo ler
        return f"Lendo o livro {self.titulo}" # Retorno do Metodo ler

# Criando objeto
meu_livro = Livro("O senhor dos Anéis") # Passando parametros
print(meu_livro.ler()) # Saida: Lendo o livro