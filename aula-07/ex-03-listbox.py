import tkinter as tk

janela = tk.Tk()

# Criando uma listbox
listbox = tk.Listbox(janela, height=5, width=30, font= ("Arial", 10))
listbox.pack()

# Adicionando itens
listbox.insert(1, "Python")
listbox.insert(2, "Java")
listbox.insert(3, "JavaScript")
listbox.insert(4, "C++")
listbox.insert(5, "Ruby")

# Adicioar no final
listbox.insert("end", "PHP")

# Pegar item selecionado
def pegar_selecionado():
    selecao = listbox.curselection()
    print("Item selecionado:", selecao) # Retorna tupla com o índice selecionado
    if selecao:
        indice = selecao[0]
        valor = listbox.get(indice)
        print(f"Selecionado: {valor} (Índice: {indice})")
    else:
        print("Nada selecionado")

# Remover item selecionado
def remover_selecionado():
    selecao = listbox.curselection()
    if selecao:
        listbox.delete(selecao[0])

btn_mostrar = tk.Button(janela, text="Mostrar Selecionado", command=pegar_selecionado)
btn_mostrar.pack()

btn_remover = tk.Button(janela, text="Remover Selecionado", command=remover_selecionado)
btn_remover.pack()

janela.mainloop()