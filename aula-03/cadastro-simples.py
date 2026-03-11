import tkinter as tk
from tkinter import messagebox

def mostrar_dados():
    nome = entry_nome.get()
    idade = entry_idade.get()
    
    if nome and idade:
        resultado.config(text=f"Nome: {nome} | Idade: {idade} anos")
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    resultado.config(text="")

# Criar janela
janela = tk.Tk()
janela.title("Sistema de Cadastro")
janela.geometry("400x300")

# Titulo
titulo = tk.Label(janela, text="Cadastro de Pessoas", font=("Arial", 14, "bold"))
titulo.pack(pady=10)

# Frame para organizar os campos
frame_campos = tk.Frame(janela)
frame_campos.pack(pady=20)

# Campo nome
tk.Label(frame_campos, text="Nome:", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_nome = tk.Entry(frame_campos, width=30)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

# Campo idade
tk.Label(frame_campos, text="Idade:", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_idade = tk.Entry(frame_campos, width=30)
entry_idade.grid(row=1, column=1, padx=5, pady=5)

# Frame botoes
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_mostrar = tk.Button(frame_botoes, text="Mostar Dados", command=mostrar_dados, bg="green", fg="white")
btn_mostrar.grid(row=0, column=1, padx=5)

btn_limpar = tk.Button(frame_botoes, text="Limpar", command=limpar_campos, bg="red", fg="white")
btn_limpar.grid(row=1, column=1, padx=5)

# Rotulo de resultados
resultado = tk.Label(janela, text="", font=("Arial", 11), fg="blue")
resultado.pack(pady=20)

janela.mainloop()