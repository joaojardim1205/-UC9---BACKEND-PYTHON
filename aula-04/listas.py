import tkinter as tk

janela = tk.Tk()
janela.title("Minha Lista de Compras")
janela.geometry("350x400")

itens = []
labels_itens = []

tk.Label(janela, text="Item:").pack(pady=(10, 0))
entry_item = tk.Entry(janela, justify="center")
entry_item.pack()

tk.Label(janela, text="Quantidade:").pack(pady=(5, 0))
entry_qtd = tk.Entry(janela, justify="center")
entry_qtd.pack()

label_erro = tk.Label(janela, text="", fg="red")
label_erro.pack()

frame_lista = tk.Frame(janela)
frame_lista.pack()

label_total = tk.Label(janela, text="Total: 0 itens", font=("Arial", 10, "bold"))
label_total.pack(pady=(5, 0))

def atualizar_total():
    label_total.config(text=f"Total: {len(itens)} itens")

def adicionar():
    label_erro.config(text="")
    nome = entry_item.get().strip()
    qtd_str = entry_qtd.get().strip()

    if not nome:
        label_erro.config(text="Digite o nome do item.")
        return

    if qtd_str == "":
        qtd = 1
    else:
        try:
            qtd = int(qtd_str)
            if qtd <= 0:
                raise ValueError
        except ValueError:
            label_erro.config(text="Quantidade deve ser inteiro positivo.")
            return

    texto = f"{qtd} {nome}"
    itens.append(texto)

    label = tk.Label(frame_lista, text=texto)
    label.pack()
    labels_itens.append(label)

    entry_item.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    atualizar_total()

def remover_ultimo():
    if labels_itens:
        labels_itens[-1].destroy()
        labels_itens.pop()
        itens.pop()
        atualizar_total()

def limpar_lista():
    for label in labels_itens:
        label.destroy()
    labels_itens.clear()
    itens.clear()
    atualizar_total()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=8)
tk.Button(frame_botoes, text="Adicionar", command=adicionar).pack(side="left", padx=4)
tk.Button(frame_botoes, text="Remover Último", command=remover_ultimo).pack(side="left", padx=4)
tk.Button(frame_botoes, text="Limpar Lista", command=limpar_lista).pack(side="left", padx=4)

janela.mainloop()