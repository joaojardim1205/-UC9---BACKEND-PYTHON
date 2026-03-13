from logging import root
import sqlite3
import tkinter as tk
from tkinter import messagebox

class CadastroProdutos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro de Produtos")
        self.janela.geometry("280x200")

    def criar_tabela(self):
        conexao = sqlite3.connect("produtos.db")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)

        conexao.commit()
        conexao.close()

    def salvar_produto(self):
        nome = entry_nome.get()
        preco = entry_preco.get()
        quantidade = entry_quantidade.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do produto é obrigatório.")
            return

        conexao = sqlite3.connect("produtos.db")
        cursor = conexao.cursor()
        
        cursor.execute("INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)", (nome, preco, quantidade))
        
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")

        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    def listar_produtos(self):
        conexao = sqlite3.connect("produtos.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM produtos")

        produtos = cursor.fetchall()
        conexao.close()

        lista_produtos = "ID\tNome\tPreço\tQuantidade\n"
        lista_produtos += "-" * 51 + "\n"

        for produto in produtos:
            lista_produtos += f"{produto[0]}\t{produto[1]}\t{produto[2]:.2f}\t{produto[3]}\n"

        messagebox.showinfo("Lista de Produtos", lista_produtos)

janela = tk.Tk()
app = CadastroProdutos(janela)
app.criar_tabela()

label_nome = tk.Label(janela, text="Nome:")
entry_nome = tk.Entry(janela)

label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_preco = tk.Label(janela, text="Preço:")
entry_preco = tk.Entry(janela)

label_preco.grid(row=1, column=0, padx=10, pady=10)
entry_preco.grid(row=1, column=1, padx=10, pady=10)

label_quantidade = tk.Label(janela, text="Quantidade:")
entry_quantidade = tk.Entry(janela)

label_quantidade.grid(row=2, column=0, padx=10, pady=10)
entry_quantidade.grid(row=2, column=1, padx=10, pady=10)

button_salvar = tk.Button(janela, text="Salvar Produto", command=app.salvar_produto)
button_salvar.grid(row=3, column=0, padx=25, pady=20)

button_listar = tk.Button(janela, text="Listar Produtos", command=app.listar_produtos)
button_listar.grid(row=3, column=1, padx=20, pady=20)

janela.mainloop()