import tkinter as tk

def ao_selecionar(event):
    listbox = event.widget
    selecao = listbox.curselection()
    if selecao:
        indice = selecao[0]
        valor = listbox.get(indice)
        label.config(text=f"Selecionado: {valor}")

janela = tk.Tk()

listbox = tk.Listbox(janela, height=5)
listbox.pack()

for i in ["Item 1", "Item 2", "Item 3", "Item 4"]:
    listbox.insert("end", i)

# Bind do evento de seleção
listbox.bind("<<ListboxSelect>>", ao_selecionar)

label = tk.Label(janela, text="Nada selecionado")
label.pack()

janela.mainloop()