import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class SistemaProdutosCRUD:

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📦 Sistema de Gerenciamento de Produtos - CRUD")
        self.janela.geometry("800x650")

        self.produto_editando_id = None

        self.criar_banco_dados()
        self.criar_interface()
        self.carregar_lista_produtos()
        self.inserir_dados_exemplo()

    def criar_banco_dados(self):
        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    preco REAL,
                    quantidade INTEGER,
                    categoria TEXT,
                    data_cadastro TEXT,
                    data_atualizacao TEXT
                )
            """)

            conexao.commit()
            conexao.close()
            print("Banco de dados criado/verificado")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao criar banco: {erro}")

    def inserir_dados_exemplo(self):
        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT COUNT(*) FROM produtos")
            total = cursor.fetchone()[0]

            if total == 0:
                produtos_exemplo = [
                    ("Notebook Dell", "Notebook com 16GB RAM e SSD 512GB", 3500.00, 10, "Eletrônicos"),
                    ("Mouse Gamer", "Mouse com RGB e 6 botões programáveis", 129.90, 25, "Informática"),
                    ("Teclado Mecânico", "Teclado com switches blue e RGB", 299.90, 15, "Informática"),
                    ("Monitor 24\"", "Monitor Full HD com 75Hz", 899.90, 8, "Eletrônicos"),
                    ("Cadeira Gamer", "Cadeira ergonômica com ajuste de altura", 1200.00, 5, "Móveis")
                ]

                for produto in produtos_exemplo:
                    cursor.execute("""
                        INSERT INTO produtos (nome, descricao, preco, quantidade, categoria, data_cadastro)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (produto[0], produto[1], produto[2], produto[3], produto[4],
                          datetime.now().strftime("%d/%m/%Y %H:%M")))

                conexao.commit()
                print(f"{len(produtos_exemplo)} produtos de exemplo inseridos")

            conexao.close()

        except sqlite3.Error as erro:
            print(f"Erro ao inserir exemplos: {erro}")

    def criar_produto(self):
        nome = self.entry_nome.get().strip()
        descricao = self.text_descricao.get("1.0", "end-1c").strip()
        preco = self.entry_preco.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        categoria = self.categoria_var.get()

        if not nome:
            messagebox.showwarning("Campo Obrigatório", "O nome do produto é obrigatório!")
            self.entry_nome.focus()
            return

        if not preco:
            messagebox.showwarning("Campo Obrigatório", "O preço do produto é obrigatório!")
            self.entry_preco.focus()
            return

        try:
            preco = float(preco)
            if preco <= 0:
                messagebox.showwarning("Valor Inválido", "O preço deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showwarning("Valor Inválido", "Digite um preço válido!")
            return

        if quantidade:
            try:
                quantidade = int(quantidade)
                if quantidade < 0:
                    messagebox.showwarning("Valor Inválido", "A quantidade não pode ser negativa!")
                    return
            except ValueError:
                messagebox.showwarning("Valor Inválido", "Digite uma quantidade válida!")
                return
        else:
            quantidade = 0

        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

            cursor.execute("""
                INSERT INTO produtos (nome, descricao, preco, quantidade, categoria, data_cadastro, data_atualizacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, descricao, preco, quantidade, categoria, data_atual, data_atual))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Produto '{nome}' criado com sucesso!")
            self.limpar_formulario()
            self.carregar_lista_produtos()
            self.atualizar_status(f"Produto '{nome}' criado")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao criar produto: {erro}")

    def ler_produtos(self):
        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, nome, preco, quantidade, categoria
                FROM produtos
                ORDER BY nome
            """)

            self.produtos = cursor.fetchall()
            conexao.close()

            self.preencher_listbox(self.produtos)
            self.atualizar_estatisticas()
            self.atualizar_status(f"{len(self.produtos)} produtos carregados")

        except sqlite3.Error as erro:
            self.atualizar_status(f"Erro ao carregar: {erro}")

    def carregar_lista_produtos(self):
        self.ler_produtos()

    def selecionar_produto_para_edicao(self, event):
        selecao = self.listbox_produtos.curselection()
        if not selecao:
            return

        texto = self.listbox_produtos.get(selecao[0])

        if texto.startswith("═") or texto == "Nenhum produto encontrado":
            return

        try:
            id_str = texto.split("]")[0].replace("[", "")
            self.produto_editando_id = int(id_str)

            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (self.produto_editando_id,))
            produto = cursor.fetchone()
            conexao.close()

            if produto:
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, produto[1])

                self.text_descricao.delete("1.0", tk.END)
                self.text_descricao.insert("1.0", produto[2] if produto[2] else "")

                self.entry_preco.delete(0, tk.END)
                self.entry_preco.insert(0, str(produto[3]))

                self.entry_quantidade.delete(0, tk.END)
                self.entry_quantidade.insert(0, str(produto[4]) if produto[4] else "0")

                self.categoria_var.set(produto[5] if produto[5] else "Eletrônicos")

                self.modo_edicao(True)

                self.atualizar_status(f"Editando produto: {produto[1]}")

        except (ValueError, IndexError, sqlite3.Error) as erro:
            self.atualizar_status(f"Erro ao selecionar: {erro}")

    def atualizar_produto(self):
        if not self.produto_editando_id:
            messagebox.showwarning("Aviso", "Nenhum produto selecionado para edição!")
            return

        nome = self.entry_nome.get().strip()
        descricao = self.text_descricao.get("1.0", "end-1c").strip()
        preco = self.entry_preco.get().strip()
        quantidade = self.entry_quantidade.get().strip()
        categoria = self.categoria_var.get()

        if not nome:
            messagebox.showwarning("Campo Obrigatório", "O nome do produto é obrigatório!")
            return

        try:
            preco = float(preco)
            if preco <= 0:
                messagebox.showwarning("Valor Inválido", "O preço deve ser maior que zero!")
                return
        except ValueError:
            messagebox.showwarning("Valor Inválido", "Digite um preço válido!")
            return

        if quantidade:
            try:
                quantidade = int(quantidade)
                if quantidade < 0:
                    messagebox.showwarning("Valor Inválido", "A quantidade não pode ser negativa!")
                    return
            except ValueError:
                messagebox.showwarning("Valor Inválido", "Digite uma quantidade válida!")
                return
        else:
            quantidade = 0

        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            data_atualizacao = datetime.now().strftime("%d/%m/%Y %H:%M")

            cursor.execute("""
                UPDATE produtos
                SET nome = ?, descricao = ?, preco = ?, quantidade = ?,
                    categoria = ?, data_atualizacao = ?
                WHERE id = ?
            """, (nome, descricao, preco, quantidade, categoria, data_atualizacao,
                  self.produto_editando_id))

            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso!")
            self.limpar_formulario()
            self.carregar_lista_produtos()
            self.atualizar_status(f"Produto '{nome}' atualizado")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao atualizar: {erro}")

    def deletar_produto(self):
        if not self.produto_editando_id:
            selecao = self.listbox_produtos.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um produto para deletar!")
                return

            texto = self.listbox_produtos.get(selecao[0])
            if texto.startswith("═") or texto == "Nenhum produto encontrado":
                messagebox.showwarning("Aviso", "Selecione um produto válido!")
                return

            try:
                id_str = texto.split("]")[0].replace("[", "")
                self.produto_editando_id = int(id_str)
            except (ValueError, IndexError):
                messagebox.showerror("Erro", "Erro ao identificar o produto!")
                return

        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM produtos WHERE id = ?", (self.produto_editando_id,))
            produto = cursor.fetchone()
            conexao.close()

            if not produto:
                messagebox.showwarning("Aviso", "Produto não encontrado!")
                self.cancelar_edicao()
                return

            resposta = messagebox.askyesno(
                "Confirmar Exclusão",
                f"⚠️ ATENÇÃO!\n\nTem certeza que deseja excluir permanentemente o produto\n\n'{produto[0]}'?\n\nEsta ação não pode ser desfeita!",
                icon="warning"
            )

            if resposta:
                conexao = sqlite3.connect("produtos_crud.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM produtos WHERE id = ?", (self.produto_editando_id,))
                conexao.commit()
                conexao.close()

                messagebox.showinfo("Sucesso", f"Produto '{produto[0]}' excluído com sucesso!")
                self.cancelar_edicao()
                self.carregar_lista_produtos()
                self.atualizar_status(f"Produto '{produto[0]}' excluído")
            else:
                self.atualizar_status("Exclusão cancelada")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao deletar: {erro}")

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="📦 SISTEMA CRUD - GERENCIAMENTO DE PRODUTOS",
            font=("Arial", 14, "bold"),
            fg="darkblue"
        )
        titulo.pack(pady=10)

        frame_form = tk.LabelFrame(self.janela, text="Formulário de Produto", padx=15, pady=10)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Nome do Produto:*", font=("Arial", 10, "bold")).grid(
            row=0, column=0, pady=5, sticky="w")
        self.entry_nome = tk.Entry(frame_form, width=50, font=("Arial", 10))
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        tk.Label(frame_form, text="Categoria:", font=("Arial", 10)).grid(
            row=1, column=0, pady=5, sticky="w")

        self.categoria_var = tk.StringVar(value="Eletrônicos")
        categorias = ["Eletrônicos", "Informática", "Móveis", "Áudio", "Acessórios", "Outros"]

        frame_cat = tk.Frame(frame_form)
        frame_cat.grid(row=1, column=1, pady=5, sticky="w")

        for i, cat in enumerate(categorias):
            tk.Radiobutton(
                frame_cat, text=cat, variable=self.categoria_var, value=cat
            ).grid(row=0, column=i, padx=5)

        tk.Label(frame_form, text="Preço (R$):*", font=("Arial", 10)).grid(
            row=2, column=0, pady=5, sticky="w")
        self.entry_preco = tk.Entry(frame_form, width=15, font=("Arial", 10))
        self.entry_preco.grid(row=2, column=1, pady=5, padx=5, sticky="w")

        tk.Label(frame_form, text="Quantidade:", font=("Arial", 10)).grid(
            row=2, column=2, pady=5, padx=(20, 0), sticky="w")
        self.entry_quantidade = tk.Entry(frame_form, width=10, font=("Arial", 10))
        self.entry_quantidade.grid(row=2, column=3, pady=5, padx=5, sticky="w")

        tk.Label(frame_form, text="Descrição:", font=("Arial", 10)).grid(
            row=3, column=0, pady=5, sticky="w")

        self.text_descricao = tk.Text(frame_form, height=4, width=60, font=("Arial", 9), wrap="word")
        self.text_descricao.grid(row=3, column=1, columnspan=3, pady=5, padx=5, sticky="ew")

        frame_botoes_form = tk.Frame(frame_form)
        frame_botoes_form.grid(row=4, column=0, columnspan=4, pady=10)

        self.btn_criar = tk.Button(
            frame_botoes_form, text="➕ CRIAR PRODUTO", command=self.criar_produto,
            bg="green", fg="white", font=("Arial", 10, "bold"), padx=15
        )
        self.btn_criar.pack(side="left", padx=5)

        self.btn_atualizar = tk.Button(
            frame_botoes_form, text="✏️ ATUALIZAR", command=self.atualizar_produto,
            bg="blue", fg="white", font=("Arial", 10, "bold"), padx=15, state="disabled"
        )
        self.btn_atualizar.pack(side="left", padx=5)

        self.btn_cancelar = tk.Button(
            frame_botoes_form, text="❌ CANCELAR", command=self.cancelar_edicao,
            bg="gray", fg="white", font=("Arial", 10, "bold"), padx=15, state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=5)

        frame_lista = tk.LabelFrame(self.janela, text="Lista de Produtos", padx=10, pady=10)
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_produtos = tk.Listbox(
            frame_lista,
            font=("Courier", 9),
            height=12,
            yscrollcommand=scrollbar.set,
            selectmode="single"
        )
        self.listbox_produtos.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_produtos.yview)

        self.listbox_produtos.bind("<<ListboxSelect>>", self.selecionar_produto_para_edicao)

        frame_botoes_lista = tk.Frame(self.janela)
        frame_botoes_lista.pack(pady=5)

        self.btn_deletar = tk.Button(
            frame_botoes_lista, text="🗑 DELETAR PRODUTO SELECIONADO", command=self.deletar_produto,
            bg="red", fg="white", font=("Arial", 10, "bold"), padx=20
        )
        self.btn_deletar.pack()

        frame_stats = tk.LabelFrame(self.janela, text="Estatísticas", padx=10, pady=5)
        frame_stats.pack(pady=5, padx=10, fill="x")

        self.label_total = tk.Label(frame_stats, text="Total: 0 produtos", font=("Arial", 10, "bold"))
        self.label_total.pack(side="left", padx=20)

        self.label_valor_total = tk.Label(frame_stats, text="Valor em estoque: R$ 0,00", font=("Arial", 10, "bold"))
        self.label_valor_total.pack(side="left", padx=20)

        self.label_preco_medio = tk.Label(frame_stats, text="Preço médio: R$ 0,00", font=("Arial", 10, "bold"))
        self.label_preco_medio.pack(side="left", padx=20)

        self.label_status = tk.Label(
            self.janela,
            text="Pronto - Modo: CADASTRO",
            font=("Arial", 9),
            fg="gray",
            relief="sunken",
            anchor="w",
            padx=5
        )
        self.label_status.pack(side="bottom", fill="x", padx=10, pady=5)

    def preencher_listbox(self, produtos):
        self.listbox_produtos.delete(0, tk.END)

        if not produtos:
            self.listbox_produtos.insert(tk.END, "Nenhum produto encontrado")
            return

        self.listbox_produtos.insert(tk.END, " ID  │ NOME PRODUTO                   │  PREÇO   │ QTD │ CATEGORIA")
        self.listbox_produtos.insert(tk.END, "─────┼────────────────────────────────┼──────────┼─────┼──────────────")

        for produto in produtos:
            id_str = f"[{produto[0]:03d}]"
            nome = produto[1][:28].ljust(28) if produto[1] else "-".ljust(28)
            preco = f"R$ {produto[2]:.2f}".rjust(8)
            qtd = str(produto[3]).rjust(3) if produto[3] is not None else "-".rjust(3)
            cat = (produto[4][:12] if produto[4] else "-").ljust(12)

            linha = f"{id_str} │ {nome} │ {preco} │ {qtd} │ {cat}"
            self.listbox_produtos.insert(tk.END, linha)

    def atualizar_estatisticas(self):
        try:
            conexao = sqlite3.connect("produtos_crud.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT COUNT(*), SUM(preco * quantidade), AVG(preco) FROM produtos")
            resultado = cursor.fetchone()
            conexao.close()

            total = resultado[0] or 0
            valor_estoque = resultado[1] or 0
            preco_medio = resultado[2] or 0

            self.label_total.config(text=f"Total: {total} produtos")
            self.label_valor_total.config(text=f"Valor em estoque: R$ {valor_estoque:.2f}")
            self.label_preco_medio.config(text=f"Preço médio: R$ {preco_medio:.2f}")

        except sqlite3.Error as erro:
            self.atualizar_status(f"Erro nas estatísticas: {erro}")

    def modo_edicao(self, ativo):
        if ativo:
            self.btn_criar.config(state="disabled")
            self.btn_atualizar.config(state="normal")
            self.btn_cancelar.config(state="normal")
            self.btn_deletar.config(state="normal")
            self.atualizar_status(f"Modo: EDIÇÃO - Produto ID {self.produto_editando_id}")
        else:
            self.btn_criar.config(state="normal")
            self.btn_atualizar.config(state="disabled")
            self.btn_cancelar.config(state="disabled")
            self.atualizar_status("Modo: CADASTRO")

    def cancelar_edicao(self):
        self.limpar_formulario()
        self.produto_editando_id = None
        self.modo_edicao(False)
        self.listbox_produtos.selection_clear(0, tk.END)
        self.atualizar_status("Edição cancelada - Modo: CADASTRO")

    def limpar_formulario(self):
        self.entry_nome.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)
        self.categoria_var.set("Eletrônicos")
        self.entry_nome.focus()

    def atualizar_status(self, mensagem):
        if hasattr(self, 'label_status'):
            self.label_status.config(text=mensagem)
            self.janela.update_idletasks()
        else:
            print(f"[STATUS] {mensagem}")


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = SistemaProdutosCRUD(janela_principal)
    janela_principal.mainloop()