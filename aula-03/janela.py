import tkinter as tk

# Definicao da janela
janela = tk.Tk()
janela.title("Minha Primeira Aplicação Desktop")

# Configuracao do tamanho da janela
janela.geometry("400x300")
janela.configure(bg="lightblue")
janela.resizable(False, False)

# Centralizacao da janela na tela
largura_janela = 400
altura_janela = 300

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenwidth()

pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2

# Exemplo
janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

# Criacao do rotulo(label)
rotulo = tk.Label(
    janela,
    text="Bem-vindo ao Python Desktop!",
    font=("Arial", 16, "bold"),
    bg="lightblue"
)
rotulo.pack(expand=True)

# Inicializacao do loop principal
janela.mainloop()