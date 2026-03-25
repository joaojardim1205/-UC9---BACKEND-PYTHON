import tkinter as tk

janela = tk.Tk()

# Criando um Entry
entry_nome = tk.Entry(janela, width=30, font=("Arial", 12))
entry_nome.pack()

# Inserindo um texto padrão
entry_nome.insert(0, "Digite seu nome aqui")

# Pegando o valor digitado
def mostrar_valor():
    valor = entry_nome.get()
    print(f"Valor digitado: {valor}")

btn = tk.Button(janela, text="Mostrar", command=mostrar_valor)
btn.pack()

janela.mainloop()