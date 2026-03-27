import tkinter as tk
from tkinter import messagebox
import sqlite3


class Biblioteca:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Biblioteca Pessoal")
        self.janela.geometry("600x560")

        self.criar_banco()
        self.criar_interface()
        self.listar_livros()
        
    def criar_banco(self):
        conexao = sqlite3.connect("biblioteca.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT    NOT NULL,
                autor  TEXT    NOT NULL,
                ano    INTEGER NOT NULL,
                status TEXT    NOT NULL DEFAULT 'Não lido'
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_interface(self):
        # Título
        tk.Label(
            self.janela,
            text="BIBLIOTECA PESSOAL",
            font=("Arial", 14, "bold"),
            fg="darkblue"
        ).pack(pady=10)

        frame_titulo = tk.Frame(self.janela)
        frame_titulo.pack(pady=4)

        tk.Label(frame_titulo, text="Título:", font=("Arial", 10), width=8, anchor="e").pack(side="left")
        self.entry_titulo = tk.Entry(frame_titulo, width=35, font=("Arial", 10))
        self.entry_titulo.pack(side="left", padx=5)

        frame_autor = tk.Frame(self.janela)
        frame_autor.pack(pady=4)

        tk.Label(frame_autor, text="Autor:", font=("Arial", 10), width=8, anchor="e").pack(side="left")
        self.entry_autor = tk.Entry(frame_autor, width=35, font=("Arial", 10))
        self.entry_autor.pack(side="left", padx=5)

        frame_ano = tk.Frame(self.janela)
        frame_ano.pack(pady=4)

        tk.Label(frame_ano, text="Ano:", font=("Arial", 10), width=8, anchor="e").pack(side="left")
        self.entry_ano = tk.Entry(frame_ano, width=10, font=("Arial", 10))
        self.entry_ano.pack(side="left", padx=5)

        frame_status = tk.Frame(self.janela)
        frame_status.pack(pady=4)

        tk.Label(frame_status, text="Status:", font=("Arial", 10), width=8, anchor="e").pack(side="left")

        self.status = tk.StringVar(value="Não lido")
        for valor in ["Lido", "Não lido"]:
            tk.Radiobutton(
                frame_status,
                text=valor,
                variable=self.status,
                value=valor,
                font=("Arial", 10)
            ).pack(side="left", padx=5)

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        tk.Button(
            frame_botoes,
            text="Adicionar Livro",
            command=self.adicionar_livro,
            bg="green", fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes,
            text="Marcar como Lido/Não Lido",
            command=self.alternar_status,
            bg="steelblue", fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar_campos,
            bg="orange", fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        tk.Label(self.janela, text="Livros Cadastrados:", font=("Arial", 10)).pack()

        frame_lista = tk.Frame(self.janela)
        frame_lista.pack(pady=5, fill="both", expand=True, padx=10)

        self.listbox_livros = tk.Listbox(
            frame_lista,
            height=10,
            font=("Arial", 10),
            selectmode="single"
        )
        self.listbox_livros.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_livros.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_livros.yview)

        self.listbox_livros.bind("<<ListboxSelect>>", self.mostrar_detalhes)

        frame_detalhes = tk.Frame(self.janela)
        frame_detalhes.pack(pady=5)

        self.label_titulo  = tk.Label(frame_detalhes, text="", font=("Arial", 9), fg="gray", justify="left")
        self.label_autor   = tk.Label(frame_detalhes, text="", font=("Arial", 9), fg="gray", justify="left")
        self.label_ano     = tk.Label(frame_detalhes, text="", font=("Arial", 9), fg="gray", justify="left")
        self.label_status  = tk.Label(frame_detalhes, text="", font=("Arial", 9), fg="gray", justify="left")

        for lbl in (self.label_titulo, self.label_autor, self.label_ano, self.label_status):
            lbl.pack(anchor="w")

    def adicionar_livro(self):
        titulo = self.entry_titulo.get().strip()
        autor  = self.entry_autor.get().strip()
        ano    = self.entry_ano.get().strip()
        status = self.status.get()

        if not titulo:
            messagebox.showwarning("Aviso", "Informe o título do livro.")
            return

        if not autor:
            messagebox.showwarning("Aviso", "Informe o autor.")
            return

        if not ano.isdigit():
            messagebox.showwarning("Aviso", "Ano deve ser um número válido.")
            return

        try:
            conexao = sqlite3.connect("biblioteca.db")
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO livros (titulo, autor, ano, status) VALUES (?, ?, ?, ?)",
                (titulo, autor, int(ano), status)
            )
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Livro adicionado!")
            self.limpar_campos()
            self.listar_livros()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao salvar: {erro}")

    def alternar_status(self):
        selecao = self.listbox_livros.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um livro na lista.")
            return

        texto_item = self.listbox_livros.get(selecao[0])
        id_str = texto_item.split("]")[0].replace("[", "")

        try:
            conexao = sqlite3.connect("biblioteca.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT status FROM livros WHERE id = ?", (int(id_str),))
            livro = cursor.fetchone()

            if livro:
                novo_status = "Lido" if livro[0] == "Não lido" else "Não lido"
                cursor.execute("UPDATE livros SET status = ? WHERE id = ?", (novo_status, int(id_str)))
                conexao.commit()

            conexao.close()
            self.listar_livros()

            for i in range(self.listbox_livros.size()):
                if self.listbox_livros.get(i).startswith(f"[{id_str}]"):
                    self.listbox_livros.select_set(i)
                    self.listbox_livros.event_generate("<<ListboxSelect>>")
                    break

        except (ValueError, sqlite3.Error) as erro:
            messagebox.showerror("Erro", f"Erro ao atualizar: {erro}")

    def listar_livros(self):
        self.listbox_livros.delete(0, tk.END)

        try:
            conexao = sqlite3.connect("biblioteca.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, titulo, autor, ano FROM livros ORDER BY titulo")
            livros = cursor.fetchall()
            conexao.close()

            for livro in livros:
                texto = f"[{livro[0]}] {livro[1]} - {livro[2]} ({livro[3]})"
                self.listbox_livros.insert(tk.END, texto)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao listar: {erro}")

    def mostrar_detalhes(self, event):
        selecao = self.listbox_livros.curselection()
        if not selecao:
            return

        texto_item = self.listbox_livros.get(selecao[0])
        id_str = texto_item.split("]")[0].replace("[", "")

        try:
            conexao = sqlite3.connect("biblioteca.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM livros WHERE id = ?", (int(id_str),))
            livro = cursor.fetchone()
            conexao.close()

            if livro:
                self.label_titulo.config(text=f"Título: {livro[1]}")
                self.label_autor.config(text=f"Autor: {livro[2]}")
                self.label_ano.config(text=f"Ano: {livro[3]}")
                self.label_status.config(text=f"Status: {livro[4]}")

        except (ValueError, sqlite3.Error):
            self.label_titulo.config(text="Erro ao carregar detalhes.")

    def limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.status.set("Não lido")
        for lbl in (self.label_titulo, self.label_autor, self.label_ano, self.label_status):
            lbl.config(text="")
        self.entry_titulo.focus()

janela = tk.Tk()
app = Biblioteca(janela)
janela.mainloop()