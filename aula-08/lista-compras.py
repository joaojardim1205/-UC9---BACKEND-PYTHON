
import tkinter as tk
from tkinter import messagebox
import sqlite3


class ListaCompras:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Lista de Compras")
        self.janela.geometry("600x500")

        self.criar_banco()
        self.criar_interface()
        self.listar_itens()

    def criar_banco(self):
        conexao = sqlite3.connect("compras.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                nome       TEXT    NOT NULL,
                quantidade INTEGER NOT NULL,
                categoria  TEXT    NOT NULL
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_interface(self):
        tk.Label(
            self.janela,
            text="LISTA DE COMPRAS",
            font=("Arial", 14, "bold"),
            fg="darkgreen"
        ).pack(pady=10)

        frame_nome = tk.Frame(self.janela)
        frame_nome.pack(pady=5)

        tk.Label(frame_nome, text="Produto:", font=("Arial", 10)).pack(side="left")
        self.entry_nome = tk.Entry(frame_nome, width=30, font=("Arial", 10))
        self.entry_nome.pack(side="left", padx=5)

        frame_qtd = tk.Frame(self.janela)
        frame_qtd.pack(pady=5)

        tk.Label(frame_qtd, text="Quantidade:", font=("Arial", 10)).pack(side="left")
        self.entry_quantidade = tk.Entry(frame_qtd, width=10, font=("Arial", 10))
        self.entry_quantidade.pack(side="left", padx=5)

        tk.Label(self.janela, text="Categoria:", font=("Arial", 10)).pack(pady=(10, 2))

        self.listbox_categorias = tk.Listbox(
            self.janela,
            height=4,
            font=("Arial", 10),
            selectmode="single",
            exportselection=False
        )
        self.listbox_categorias.pack()

        for cat in ["Hortifrúti", "Mercearia", "Limpeza", "Bebidas"]:
            self.listbox_categorias.insert(tk.END, cat)

        self.listbox_categorias.select_set(0)

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        tk.Button(
            frame_botoes,
            text="Adicionar Item",
            command=self.adicionar_item,
            bg="green", fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes,
            text="Remover Selecionado",
            command=self.remover_item,
            bg="red", fg="white",
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

        tk.Label(self.janela, text="Itens na Lista:", font=("Arial", 10)).pack()

        frame_lista = tk.Frame(self.janela)
        frame_lista.pack(pady=5, fill="both", expand=True, padx=10)

        self.listbox_itens = tk.Listbox(
            frame_lista,
            height=8,
            font=("Arial", 10),
            selectmode="single"
        )
        self.listbox_itens.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_itens.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_itens.yview)

        self.listbox_itens.bind("<<ListboxSelect>>", self.mostrar_detalhes)

        self.label_detalhes = tk.Label(
            self.janela,
            text="",
            font=("Arial", 9),
            justify="left",
            fg="gray"
        )
        self.label_detalhes.pack(pady=5)

    def adicionar_item(self):
        nome = self.entry_nome.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        selecao_cat = self.listbox_categorias.curselection()

        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do produto.")
            return

        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showwarning("Aviso", "Quantidade deve ser um número maior que zero.")
            return

        if not selecao_cat:
            messagebox.showwarning("Aviso", "Selecione uma categoria.")
            return

        categoria = self.listbox_categorias.get(selecao_cat[0])

        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO itens (nome, quantidade, categoria) VALUES (?, ?, ?)",
                (nome, int(quantidade), categoria)
            )
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Item adicionado!")
            self.limpar_campos()
            self.listar_itens()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao salvar: {erro}")

    def remover_item(self):
        selecao = self.listbox_itens.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um item para remover.")
            return

        texto_item = self.listbox_itens.get(selecao[0])
        id_str = texto_item.split("]")[0].replace("[", "")

        if not messagebox.askyesno("Confirmar", "Deseja remover o item selecionado?"):
            return

        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM itens WHERE id = ?", (int(id_str),))
            conexao.commit()
            conexao.close()

            self.label_detalhes.config(text="")
            self.listar_itens()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao remover: {erro}")

    def listar_itens(self):
        self.listbox_itens.delete(0, tk.END)

        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, quantidade, categoria FROM itens ORDER BY categoria")
            itens = cursor.fetchall()
            conexao.close()

            for item in itens:
                texto = f"[{item[0]}] {item[1]} x{item[2]} ({item[3]})"
                self.listbox_itens.insert(tk.END, texto)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao listar: {erro}")

    def mostrar_detalhes(self, event):
        selecao = self.listbox_itens.curselection()
        if not selecao:
            return

        texto_item = self.listbox_itens.get(selecao[0])
        id_str = texto_item.split("]")[0].replace("[", "")

        try:
            conexao = sqlite3.connect("compras.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM itens WHERE id = ?", (int(id_str),))
            item = cursor.fetchone()
            conexao.close()

            if item:
                detalhes = f"ID: {item[0]}  |  Produto: {item[1]}  |  Quantidade: {item[2]}  |  Categoria: {item[3]}"
                self.label_detalhes.config(text=detalhes)

        except (ValueError, sqlite3.Error):
            self.label_detalhes.config(text="Erro ao carregar detalhes.")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.listbox_categorias.select_set(0)
        self.label_detalhes.config(text="")
        self.entry_nome.focus()


janela = tk.Tk()
app = ListaCompras(janela)
janela.mainloop()