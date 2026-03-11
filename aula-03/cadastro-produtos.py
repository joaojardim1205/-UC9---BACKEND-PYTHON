import tkinter as tk

# Janela principal
janela = tk.Tk()
janela.title("Sistema de Cadastro de Produtos")
janela.geometry("600x400")
janela.configure(bg="white")
janela.resizable(False, False)

# Título
titulo = tk.Label(janela, text="Cadastro de Produtos", font=("Arial", 18, "bold"), bg="lightblue", fg="black", pady=10)
titulo.pack(fill="x")

# Frame campos
frame_campos = tk.Frame(janela, bg="white", padx=20, pady=10)
frame_campos.pack(fill="x")

# Rotulo
def criar_campo(parent, texto, row):
    label = tk.Label(parent, text=texto, font=("Arial", 10, "bold"), bg="white", fg="black", anchor="w", width=18)
    label.grid(row=row, column=0, pady=6, sticky="w")

    entry = tk.Entry(parent, font=("Arial", 10), width=35, bd=1, relief="solid")
    entry.grid(row=row, column=1, pady=6, padx=(5, 0), sticky="w")
    return entry

# Campos de entrada
entry_nome = criar_campo(frame_campos, "Nome do Produto:", 0)
entry_descritivo = criar_campo(frame_campos, "Descritivo:", 1)
entry_quantidade = criar_campo(frame_campos, "Quantidade:", 2)
entry_fornecedor = criar_campo(frame_campos, "Fornecedor:", 3)

# Frame botões
frame_botoes = tk.Frame(janela, bg="white")
frame_botoes.pack(pady=8)

# Rótulo de resultado
label_resultado = tk.Label(janela, text="", font=("Arial", 9), bg="lightblue", fg="black", wraplength=560, justify="left", anchor="w", padx=12, pady=10, relief="flat")
label_resultado.pack(fill="x", padx=20)

# Funções botões
def mostrar_dados():
    nome = entry_nome.get()
    desc = entry_descritivo.get()
    qtd  = entry_quantidade.get()
    forn = entry_fornecedor.get()
    label_resultado.config(
        text=f"Nome do Produto: {nome} - Descritivo: {desc} - Quantidade: {qtd} - Fornecedor: {forn}"
    )

def limpar():
    entry_nome.delete(0, tk.END)
    entry_descritivo.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_fornecedor.delete(0, tk.END)
    label_resultado.config(text="")

# Botão Mostrar Dados
btn_mostrar = tk.Button(frame_botoes, text="Mostrar Dados", font=("Arial", 10, "bold"), bg="lightblue", fg="black", padx=18, pady=6, command=mostrar_dados)
btn_mostrar.pack(side="left", padx=10)

# Botão Limpar
btn_limpar = tk.Button(frame_botoes, text="Limpar", font=("Arial", 10, "bold"), bg="lightyellow", fg="black", padx=18, pady=6, command=limpar)
btn_limpar.pack(side="left", padx=10)

janela.mainloop()