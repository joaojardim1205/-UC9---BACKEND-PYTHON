import sqlite3
import tkinter as tk
from tkinter import messagebox

class AgendaContatos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Agenda de Contatos")
        self.janela.geometry("280x400")

    def criar_tabela(self):
        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT,
                categoria TEXT
            )
        """)

        conexao.commit()
        conexao.close()

    def salvar_contato(self):
        nome = entry_nome.get()
        telefone = entry_telefone.get()
        email = entry_email.get()
        categoria = categoria_var.get()

        if not nome:
            messagebox.showerror("Erro", "O nome do contato é obrigatório.")
            return

        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()

        cursor.execute("INSERT INTO contatos (nome, telefone, email, categoria) VALUES (?, ?, ?, ?)", (nome, telefone, email, categoria))

        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Contato salvo com sucesso!")

        entry_nome.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    def buscar_contatos(self):
        busca = entry_busca.get()
        conexao = sqlite3.connect("agenda.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM contatos WHERE nome LIKE ?", ('%' + busca + '%',))
        
        contatos = cursor.fetchall()
        conexao.close()

        lista_contatos = f"{'ID':<10} {'Nome':<10} {'Telefone':<25} {'Email':<20} {'Categoria'}\n"
        lista_contatos += "-" * 79 + "\n"

        for contato in contatos:
            id_, nome, telefone, email, categoria = contato
            lista_contatos += f"{id_:<10} {nome:<10} {telefone:<15} {email:<20} {categoria}\n"

        messagebox.showinfo("Contatos Encontrados", lista_contatos)

janela = tk.Tk()
app = AgendaContatos(janela)
app.criar_tabela()

label_nome = tk.Label(janela, text="Nome:")
entry_nome = tk.Entry(janela)

label_nome.grid(row=0, column=0, padx=10, pady=10)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

label_telefone = tk.Label(janela, text="Telefone:")
entry_telefone = tk.Entry(janela)

label_telefone.grid(row=1, column=0, padx=10, pady=10)
entry_telefone.grid(row=1, column=1, padx=10, pady=10)

label_email = tk.Label(janela, text="Email:")
entry_email = tk.Entry(janela)

label_email.grid(row=2, column=0, padx=10, pady=10)
entry_email.grid(row=2, column=1, padx=10, pady=10)

categoria_var = tk.StringVar(value="Amigo")
label_categoria = tk.Label(janela, text="Categoria:")
label_categoria.grid(row=3, column=0, padx=10, pady=10)

radiobutton_amigo = tk.Radiobutton(janela, text="Amigo", variable=categoria_var, value="Amigo")
radiobutton_familia = tk.Radiobutton(janela, text="Família", variable=categoria_var, value="Família")
radiobutton_trabalho = tk.Radiobutton(janela, text="Trabalho", variable=categoria_var, value="Trabalho")

radiobutton_amigo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
radiobutton_familia.grid(row=4, column=1, padx=10, pady=5, sticky="w")
radiobutton_trabalho.grid(row=5, column=1, padx=10, pady=5, sticky="w")

button_salvar = tk.Button(janela, text="Salvar Contato", command=app.salvar_contato)
button_salvar.grid(row=6, column=0, columnspan=2, pady=10)

label_busca = tk.Label(janela, text="Buscar por Nome:")
entry_busca = tk.Entry(janela)
label_busca.grid(row=7, column=0, padx=10, pady=10)
entry_busca.grid(row=7, column=1, padx=10, pady=10)

button_buscar = tk.Button(janela, text="Buscar Contatos", command=app.buscar_contatos)
button_buscar.grid(row=8, column=0, columnspan=2, pady=10)

janela.mainloop()