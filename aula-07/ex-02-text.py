import tkinter as tk

janela = tk.Tk()

# Criando uma área de texto
texto_observacoes = tk.Text(janela, height=5, width=40, font=("Arial", 12))
texto_observacoes.pack()

# Inserindo um texto inicial
texto_observacoes.insert("1.0", "Digite suas observações aqui...")

# Pegando todo o texto 
def pegar_texto():
    conteudo = texto_observacoes.get("1.0", "end-1c")  
    # end-1c remove o ultimo caracter (\n)
    print(f"Observações: {conteudo}")

# Inserindo texto em posições específicas
def inserir_texto():
    texto_observacoes.insert("end", "\n Nova linha adicionada")

btn_pegar = tk.Button(janela, text="Pegar Texto", command=pegar_texto)
btn_pegar.pack()

btn_inserir = tk.Button(janela, text="Inserir Texto", command=inserir_texto)
btn_inserir.pack()

janela.mainloop()