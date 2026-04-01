import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class SistemaConsultaProdutos:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("📦 Sistema de Consulta de Produtos")
        self.janela.geometry("800x600")

        self.todos_produtos = []
        self.label_status = None
        
        self.criar_interface()
        self.criar_banco_dados()
        self.carregar_todos_produtos()
        self.inserir_dados_exemplo()

    def criar_banco_dados(self):
        try:
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT,
                    preco REAL,
                    estoque INTEGER,
                    data_cadastro TEXT
                )
            """)

            conexao.commit()
            conexao.close()

            self.atualizar_status("Banco de dados criado/verificado com sucesso!")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Banco", f"Falha ao criar banco de dados:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def inserir_dados_exemplo(self):
        try:
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()

            cursor.execute("SELECT COUNT(*) FROM produtos")
            total = cursor.fetchone()[0]
           
            if total == 0:
                produtos_exemplo = [
                    ("Notebook Dell", "Eletrônicos", 3500.00, 10, datetime.now().strftime("%d/%m/%Y")),
                    ("Mouse Logitech", "Eletrônicos", 89.90, 25, datetime.now().strftime("%d/%m/%Y")),
                    ("Teclado Mecânico", "Eletrônicos", 299.90, 15, datetime.now().strftime("%d/%m/%Y")),
                    ("Cadeira Gamer", "Móveis", 1200.00, 5, datetime.now().strftime("%d/%m/%Y")),
                    ("Monitor 24\"", "Eletrônicos", 899.90, 8, datetime.now().strftime("%d/%m/%Y")),
                    ("Impressora Laser", "Eletrônicos", 1599.90, 3, datetime.now().strftime("%d/%m/%Y")),
                    ("Mesa Digitalizadora", "Eletrônicos", 450.00, 12, datetime.now().strftime("%d/%m/%Y")),
                    ("Fone Bluetooth", "Áudio", 199.90, 20, datetime.now().strftime("%d/%m/%Y")),
                    ("Caixa de Som", "Áudio", 349.90, 7, datetime.now().strftime("%d/%m/%Y")),
                    ("HD Externo 1TB", "Armazenamento", 399.90, 14, datetime.now().strftime("%d/%m/%Y")),
                    ("SSD 500GB", "Armazenamento", 279.90, 18, datetime.now().strftime("%d/%m/%Y")),
                    ("Webcam HD", "Eletrônicos", 159.90, 9, datetime.now().strftime("%d/%m/%Y")),
                    ("Roteador Wi-Fi", "Redes", 249.90, 6, datetime.now().strftime("%d/%m/%Y")),
                    ("Tablet", "Eletrônicos", 1299.90, 4, datetime.now().strftime("%d/%m/%Y")),
                    ("Smartwatch", "Eletrônicos", 599.90, 11, datetime.now().strftime("%d/%m/%Y"))
                ]

                cursor.executemany("""
                    INSERT INTO produtos (nome, categoria, preco, estoque, data_cadastro)
                    VALUES (?, ?, ?, ?, ?)
                """, produtos_exemplo)
                conexao.commit()

                self.atualizar_status(f"{len(produtos_exemplo)} produtos de exemplo inseridos!")
            conexao.close()

        except sqlite3.Error as erro:
            self.atualizar_status(f"Erro ao inserir dados exemplo: {erro}")

    def carregar_todos_produtos(self):
        try:
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, nome, categoria, preco, estoque
                FROM produtos
                ORDER BY nome
            """)
            self.todos_produtos = cursor.fetchall()

            self.preencher_listbox(self.todos_produtos)
            self.atualizar_estatisticas(self.todos_produtos)
            conexao.close()

            self.atualizar_status(f"{len(self.todos_produtos)} produtos carregados")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao carregar produtos:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def buscar_por_nome(self):
        try:
            termo = self.entry_busca.get().strip()
            
            if not termo:
                self.carregar_todos_produtos()
                return
            
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, nome, categoria, preco, estoque
                FROM produtos
                WHERE nome LIKE ?
                ORDER BY nome
            """, (f"%{termo}%",))
            resultados = cursor.fetchall()
            
            self.preencher_listbox(resultados)
            self.atualizar_estatisticas(resultados)

            conexao.close()

            self.atualizar_status(f"Busca por '{termo}': {len(resultados)} produtos encontrados")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro na busca:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def buscar_por_categoria(self):
        try:
            categoria = self.categoria_var.get()

            if categoria == "Todas":
                self.carregar_todos_produtos()
                return
            
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id, nome, categoria, preco, estoque
                FROM produtos
                WHERE categoria = ?
                ORDER BY nome
            """, (categoria,))
            resultados = cursor.fetchall()

            self.preencher_listbox(resultados)
            self.atualizar_estatisticas(resultados)

            conexao.close()

            self.atualizar_status(f"Categoria '{categoria}': {len(resultados)} produtos encontrados")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao filtrar:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def buscar_por_preco(self):
        try:
            preco_min = self.entry_preco_min.get().strip()
            preco_max = self.entry_preco_max.get().strip()
            
            query = "SELECT id, nome, categoria, preco, estoque FROM produtos WHERE 1=1"
            
            parametros = []
            
            if preco_min:
                try:
                    preco_min = float(preco_min)
                    query += " AND preco >= ?"
                    parametros.append(preco_min)
                except ValueError:
                    messagebox.showwarning("Aviso", "Valor mínimo inválido!")
                    return
            
            if preco_max:
                try:
                    preco_max = float(preco_max)
                    query += " AND preco <= ?"
                    parametros.append(preco_max)
                except ValueError:
                    messagebox.showwarning("Aviso", "Valor máximo inválido!")
                    return
            
            if not parametros:
                messagebox.showinfo("Aviso", "Informe pelo menos um valor de preço!")
                return
            
            query += " ORDER BY preco"
            
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()
            
            cursor.execute(query, parametros)
           
            resultados = cursor.fetchall()
           
            self.preencher_listbox(resultados)
            self.atualizar_estatisticas(resultados)
           
            conexao.close()
           
            self.atualizar_status(f"Preço entre R$ {preco_min} e R$ {preco_max}: {len(resultados)} produtos")
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro na busca:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def buscar_ordenado(self):
        try:
            campo = self.ordenar_var.get()
            
            if campo == "Nome":
                campo_sql = "nome"
            elif campo == "Preço":
                campo_sql = "preco"
            elif campo == "Estoque":
                campo_sql = "estoque"
            else:
                campo_sql = "nome"
           
            ordem = self.ordem_var.get()
            ordem_sql = "DESC" if ordem == "Decrescente" else "ASC"
          
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()
            
            cursor.execute(f"""
                SELECT id, nome, categoria, preco, estoque
                FROM produtos
                ORDER BY {campo_sql} {ordem_sql}
            """)
            resultados = cursor.fetchall()
           
            self.preencher_listbox(resultados)
            self.atualizar_estatisticas(resultados)
           
            conexao.close()
            
            self.atualizar_status(f"Ordenado por {campo} ({ordem})")
      
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro na ordenação:\n{erro}")
            self.atualizar_status(f"ERRO: {erro}")

    def preencher_listbox(self, produtos):
        self.listbox_produtos.delete(0, tk.END)
        
        if not produtos:
            self.listbox_produtos.insert(tk.END, "═" * 60)
            self.listbox_produtos.insert(tk.END, "Nenhum produto encontrado")
            self.listbox_produtos.insert(tk.END, "═" * 60)
       
            return
     
        self.listbox_produtos.insert(tk.END, " ID │ NOME PRODUTO               │ CATEGORIA     │  PREÇO │ EST")
        self.listbox_produtos.insert(tk.END, "────┼──────────────────────────────┼───────────────┼────────┼─────")
     
        for produto in produtos:
            id_prod = str(produto[0]).ljust(3)
            nome = produto[1][:28].ljust(28)
            categoria = (produto[2][:13] if produto[2] else "-").ljust(13)
            preco = f"R${produto[3]:.2f}".rjust(7)
            estoque = str(produto[4]).rjust(4)
            linha = f" {id_prod} │ {nome} │ {categoria} │ {preco} │ {estoque}"
            self.listbox_produtos.insert(tk.END, linha)

    def atualizar_estatisticas(self, produtos):
        if not produtos:
            self.label_total.config(text="Total: 0 produtos")
            self.label_valor_total.config(text="Valor total: R$ 0,00")
            self.label_estoque_total.config(text="Estoque total: 0 unidades")
            return
        
        total = len(produtos)
        valor_total = sum(p[3] for p in produtos)
        estoque_total = sum(p[4] for p in produtos)
        
        self.label_total.config(text=f"Total: {total} produtos")
        self.label_valor_total.config(text=f"Valor total: R$ {valor_total:.2f}")
        self.label_estoque_total.config(text=f"Estoque total: {estoque_total} unidades")

    def carregar_categorias_listbox(self):
        try:
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()
           
            cursor.execute("SELECT DISTINCT categoria FROM produtos ORDER BY categoria")
            categorias = cursor.fetchall()
           
            self.listbox_categorias.delete(0, tk.END)
            self.listbox_categorias.insert(tk.END, "Todas")
            
            for cat in categorias:
                if cat[0]:
                    self.listbox_categorias.insert(tk.END, cat[0])
          
            conexao.close()
        
        except sqlite3.Error as erro:
            self.atualizar_status(f"Erro ao carregar categorias: {erro}")

    def ao_selecionar_categoria(self, event):
        selecao = self.listbox_categorias.curselection()
       
        if selecao:
            categoria = self.listbox_categorias.get(selecao[0])
            self.categoria_var.set(categoria)
            self.buscar_por_categoria()

    def mostrar_detalhes_produto(self, event):
        selecao = self.listbox_produtos.curselection()
       
        if not selecao:
            return
        texto_selecionado = self.listbox_produtos.get(selecao[0])
       
        if texto_selecionado.startswith(" ID ") or texto_selecionado.startswith("──"):
            return
        try:
            id_str = texto_selecionado[1:4].strip()
            id_produto = int(id_str)
          
            conexao = sqlite3.connect("produtos_consulta.db")
            cursor = conexao.cursor()
           
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
            produto = cursor.fetchone()
          
            conexao.close()
          
            if produto:
                detalhes = f"📦 PRODUTO #{produto[0]}\n"
                detalhes += f"📝 Nome: {produto[1]}\n"
                detalhes += f"🏷 Categoria: {produto[2]}\n"
                detalhes += f"💰 Preço: R$ {produto[3]:.2f}\n"
                detalhes += f"📊 Estoque: {produto[4]} unidades\n"
                detalhes += f"📅 Cadastrado em: {produto[5]}\n"
                valor_estoque = produto[3] * produto[4]
                detalhes += f"💵 Valor em estoque: R$ {valor_estoque:.2f}"
                self.label_detalhes.config(text=detalhes)
       
        except (ValueError, IndexError, sqlite3.Error) as erro:
            self.label_detalhes.config(text=f"Erro ao carregar detalhes: {erro}")

    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="📦 SISTEMA DE CONSULTA DE PRODUTOS",
            font=("Arial", 16, "bold"),
            fg="darkblue"
        )
        titulo.pack(pady=10)

        frame_busca = tk.LabelFrame(self.janela, text="Busca Rápida", padx=10, pady=10)
        frame_busca.pack(pady=5, padx=10, fill="x")

        tk.Label(frame_busca, text="Nome:").grid(row=0, column=0, pady=5)
        self.entry_busca = tk.Entry(frame_busca, width=30)
        self.entry_busca.grid(row=0, column=1, pady=5, padx=5)

        tk.Button(
            frame_busca,
            text="🔍 Buscar",
            command=self.buscar_por_nome,
            bg="blue",
            fg="white"
        ).grid(row=0, column=2, pady=5, padx=5)

        tk.Label(frame_busca, text="Preço de:").grid(row=1, column=0, pady=5)
        self.entry_preco_min = tk.Entry(frame_busca, width=12)
        self.entry_preco_min.grid(row=1, column=1, pady=5, padx=5, sticky="w")

        tk.Label(frame_busca, text="até:").grid(row=1, column=1, pady=5, padx=(100, 0))
        self.entry_preco_max = tk.Entry(frame_busca, width=12)
        self.entry_preco_max.grid(row=1, column=1, pady=5, padx=(130, 0))

        tk.Button(
            frame_busca,
            text="💰 Buscar por Preço",
            command=self.buscar_por_preco,
            bg="green",
            fg="white"
        ).grid(row=1, column=2, pady=5, padx=5)

        frame_filtros = tk.LabelFrame(self.janela, text="Filtros Avançados", padx=10, pady=10)
        frame_filtros.pack(pady=5, padx=10, fill="x")

        tk.Label(frame_filtros, text="Categoria:").grid(row=0, column=0, pady=5, sticky="w")

        self.categoria_var = tk.StringVar(value="Todas")
        categorias = ["Todas", "Eletrônicos", "Móveis", "Áudio", "Armazenamento", "Redes"]

        frame_cats = tk.Frame(frame_filtros)
        frame_cats.grid(row=0, column=1, pady=5, sticky="w")

        for i, cat in enumerate(categorias):
            tk.Radiobutton(
                frame_cats,
                text=cat,
                variable=self.categoria_var,
                value=cat,
                command=self.buscar_por_categoria
            ).grid(row=0, column=i, padx=5)

        tk.Label(frame_filtros, text="Ordenar por:").grid(row=1, column=0, pady=5, sticky="w")

        self.ordenar_var = tk.StringVar(value="Nome")
        self.ordem_var = tk.StringVar(value="Crescente")

        tk.OptionMenu(frame_filtros, self.ordenar_var, "Nome", "Preço", "Estoque").grid(
            row=1, column=1, pady=5, sticky="w"
        )
      
        tk.OptionMenu(frame_filtros, self.ordem_var, "Crescente", "Decrescente").grid(
            row=1, column=1, pady=5, padx=(150, 0)
        )

        tk.Button(
            frame_filtros,
            text="🔄 Aplicar Ordenação",
            command=self.buscar_ordenado,
            bg="orange",
            fg="white"
        ).grid(row=1, column=2, pady=5, padx=10)

        tk.Button(
            frame_filtros,
            text="📋 Mostrar Todos",
            command=self.carregar_todos_produtos,
            bg="gray",
            fg="white"
        ).grid(row=1, column=3, pady=5, padx=10)

        frame_principal = tk.Frame(self.janela)
        frame_principal.pack(fill="both", expand=True, padx=10, pady=5)

        frame_lista = tk.LabelFrame(frame_principal, text="Lista de Produtos", padx=5, pady=5)
        frame_lista.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_produtos = tk.Listbox(
            frame_lista,
            font=("Courier", 9),
            height=20,
            yscrollcommand=scrollbar.set,
            selectmode="single"
        )
       
        self.listbox_produtos.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_produtos.yview)

        self.listbox_produtos.bind("<<ListboxSelect>>", self.mostrar_detalhes_produto)

        frame_detalhes = tk.LabelFrame(frame_principal, text="Detalhes do Produto", padx=10, pady=10)
        frame_detalhes.pack(side="right", fill="y", padx=(10, 0), ipadx=20)

        self.label_detalhes = tk.Label(
            frame_detalhes,
            text="Selecione um produto na lista\npara ver os detalhes",
            font=("Arial", 10),
            justify="left",
            relief="sunken",
            padx=10,
            pady=20
        )
        self.label_detalhes.pack()

        frame_stats = tk.LabelFrame(self.janela, text="Estatísticas", padx=10, pady=5)
        frame_stats.pack(pady=5, padx=10, fill="x")

        self.label_total = tk.Label(frame_stats, text="Total: 0 produtos", font=("Arial", 10, "bold"))
        self.label_total.pack(side="left", padx=20)

        self.label_valor_total = tk.Label(frame_stats, text="Valor total: R$ 0,00", font=("Arial", 10, "bold"))
        self.label_valor_total.pack(side="left", padx=20)

        self.label_estoque_total = tk.Label(frame_stats, text="Estoque total: 0 unidades", font=("Arial", 10, "bold"))
        self.label_estoque_total.pack(side="left", padx=20)

        self.label_status = tk.Label(
            self.janela,
            text="Pronto",
            font=("Arial", 9),
            fg="gray",
            relief="sunken",
            anchor="w",
            padx=5
        )
        self.label_status.pack(side="bottom", fill="x", padx=10, pady=5)

    def atualizar_status(self, mensagem):
        if self.label_status:
            self.label_status.config(text=mensagem)
            self.janela.update_idletasks()


if __name__ == "__main__":
    janela_principal = tk.Tk()
    app = SistemaConsultaProdutos(janela_principal)
    janela_principal.mainloop()