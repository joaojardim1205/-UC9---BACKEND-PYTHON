# SISTEMA DE CADASTRO DE FILMES
import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class CadastroFilmes:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("🎬 Meus Filmes Assistidos")
        self.janela.geometry("650x550")
        
        self.criar_banco()
        self.criar_interface()
        self.atualizar_lista()

    # MÉTODOS DO BANCO DE DADOS
    def criar_banco(self):
        try:
            conexao = sqlite3.connect("filmes.db")
            cursor = conexao.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS filmes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    ano INTEGER,
                    genero TEXT,
                    nota INTEGER,
                    comentarios TEXT,
                    data_registro TEXT
                )
            """)

            conexao.commit()
            conexao.close()
            
            print("Banco de dados criado/verificado com sucesso!")
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de Banco", f"Falha ao criar banco: {erro}")

    # MÉTODOS DA INTERFACE
    def criar_interface(self):
        titulo = tk.Label(
            self.janela,
            text="🎬 SISTEMA DE CADASTRO DE FILMES",
            font=("Arial", 14, "bold"),
            fg="darkred",
            bg="#f0f0f0"
        )
        titulo.pack(pady=10)

        frame_entrada = tk.LabelFrame(
            self.janela,
            text="Dados do Filme",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=10
        )
        frame_entrada.pack(pady=10, padx=10, fill="x")

        # Linha 1: Título
        linha1 = tk.Frame(frame_entrada)
        linha1.pack(fill="x", pady=5)
        
        tk.Label(linha1, text="Título:", width=10, anchor="w").pack(side="left")
        self.entry_titulo = tk.Entry(linha1, width=50, font=("Arial", 10))
        self.entry_titulo.pack(side="left", padx=5, fill="x", expand=True)

        # Linha 2: Ano e Gênero
        linha2 = tk.Frame(frame_entrada)
        linha2.pack(fill="x", pady=5)
        
        tk.Label(linha2, text="Ano:", width=10, anchor="w").pack(side="left")
        self.entry_ano = tk.Entry(linha2, width=15, font=("Arial", 10))
        self.entry_ano.pack(side="left", padx=5)
        
        tk.Label(linha2, text="Gênero:", width=8, anchor="w").pack(side="left", padx=(20, 0))
        self.entry_genero = tk.Entry(linha2, width=25, font=("Arial", 10))
        self.entry_genero.pack(side="left", padx=5, fill="x", expand=True)

        # Linha 3: Nota (Radiobuttons)
        linha3 = tk.Frame(frame_entrada)
        linha3.pack(fill="x", pady=5)
        
        tk.Label(linha3, text="Nota:", width=10, anchor="w").pack(side="left")
        self.nota = tk.StringVar(value="5")
        
        for i in range(1, 6):
            tk.Radiobutton(
                linha3,
                text=str(i),
                variable=self.nota,
                value=str(i)
            ).pack(side="left", padx=2)

        # Linha 4: Comentários
        linha4 = tk.Frame(frame_entrada)
        linha4.pack(fill="x", pady=5)
        
        tk.Label(linha4, text="Comentários:", width=10, anchor="w").pack(side="left")
        
        self.text_comentarios = tk.Text(
            linha4,
            height=3,
            width=40,
            font=("Arial", 9),
            wrap="word"
        )
        self.text_comentarios.pack(side="left", padx=5, fill="x", expand=True)

        # Frame de Botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        self.btn_adicionar = tk.Button(
            frame_botoes,
            text="✅ Adicionar Filme",
            command=self.adicionar_filme,
            bg="green", fg="white",
            font=("Arial", 10, "bold"),
            padx=15, cursor="hand2"
        )
        self.btn_adicionar.pack(side="left", padx=5)

        self.btn_limpar = tk.Button(
            frame_botoes,
            text="🔄 Limpar Campos",
            command=self.limpar_campos,
            bg="orange", fg="white",
            font=("Arial", 10, "bold"),
            padx=15, cursor="hand2"
        )
        self.btn_limpar.pack(side="left", padx=5)

        self.btn_remover = tk.Button(
            frame_botoes,
            text="🗑 Remover Filme",
            command=self.remover_filme,
            bg="red", fg="white",
            font=("Arial", 10, "bold"),
            padx=15, cursor="hand2"
        )
        self.btn_remover.pack(side="left", padx=5)

        # Frame da Lista
        frame_lista = tk.LabelFrame(
            self.janela,
            text="Filmes Cadastrados",
            font=("Arial", 10, "bold"),
            padx=10, pady=10
        )
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_filmes = tk.Listbox(
            frame_lista,
            height=8,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set,
            selectmode="single",
            activestyle="dotbox"
        )
        self.listbox_filmes.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_filmes.yview)

        # Bind de Eventos
        self.listbox_filmes.bind("<<ListboxSelect>>", self.mostrar_detalhes)
        self.entry_titulo.bind("<Return>", lambda e: self.entry_ano.focus())
        self.entry_ano.bind("<Return>", lambda e: self.entry_genero.focus())
        self.entry_genero.bind("<Return>", lambda e: self.text_comentarios.focus())
        self.janela.bind("<Control-a>", lambda e: self.adicionar_filme())

        # Label de Detalhes
        self.label_detalhes = tk.Label(
            self.janela,
            text="",
            font=("Arial", 9),
            justify="left",
            bg="#e0e0e0",
            relief="sunken",
            padx=5, pady=5
        )
        self.label_detalhes.pack(pady=5, padx=10, fill="x")

    # MÉTODOS DE FUNCIONALIDADE
    def adicionar_filme(self):
        titulo = self.entry_titulo.get().strip()
        ano = self.entry_ano.get().strip()
        genero = self.entry_genero.get().strip()
        nota = self.nota.get()
        comentarios = self.text_comentarios.get("1.0", "end-1c").strip()
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

        if not titulo:
            messagebox.showwarning("Campo Obrigatório", "O título do filme é obrigatório!")
            self.entry_titulo.focus()
            return

        if ano:
            try:
                ano = int(ano)
                if ano < 1888 or ano > 2030:
                    messagebox.showwarning("Ano Inválido", "Digite um ano entre 1888 e 2030!")
                    self.entry_ano.focus()
                    return
            except ValueError:
                messagebox.showwarning("Ano Inválido", "O ano deve ser um número inteiro!")
                self.entry_ano.focus()
                return

        try:
            conexao = sqlite3.connect("filmes.db")
            cursor = conexao.cursor()
            
            cursor.execute("""
                INSERT INTO filmes (titulo, ano, genero, nota, comentarios, data_registro)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (titulo, ano, genero, nota, comentarios, data_atual))
            
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", f"Filme '{titulo}' adicionado com sucesso!")
            
            self.limpar_campos()
            self.atualizar_lista()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro no Banco", f"Falha ao inserir filme: {erro}")

    def atualizar_lista(self):
        self.listbox_filmes.delete(0, tk.END)
        
        try:
            conexao = sqlite3.connect("filmes.db")
            cursor = conexao.cursor()
           
            cursor.execute("""
                SELECT id, titulo, ano, nota
                FROM filmes
                ORDER BY data_registro DESC
            """)
            filmes = cursor.fetchall()
            
            conexao.close()

            for filme in filmes:
                texto = f"[{filme[0]:03d}] {filme[1]}"
               
                if filme[2]:
                    texto += f" ({filme[2]})"
               
                texto += f" - Nota: {filme[3]}/5"
                self.listbox_filmes.insert(tk.END, texto)

            total = len(filmes)
            self.listbox_filmes.insert(tk.END, "─" * 60)
            self.listbox_filmes.insert(tk.END, f"📊 Total de filmes: {total}")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Falha ao listar filmes: {erro}")

    def mostrar_detalhes(self, event):
        selecao = self.listbox_filmes.curselection()
       
        if not selecao:
            return

        texto_item = self.listbox_filmes.get(selecao[0])
       
        try:
            id_str = texto_item.split("]")[0].replace("[", "")
            id_filme = int(id_str)

            conexao = sqlite3.connect("filmes.db")
            cursor = conexao.cursor()
           
            cursor.execute("SELECT * FROM filmes WHERE id = ?", (id_filme,))
            filme = cursor.fetchone()
           
            conexao.close()

            if filme:
                detalhes = f"🎬 ID: {filme[0]} | Título: {filme[1]}"
                if filme[2]:
                    detalhes += f" | Ano: {filme[2]}"
                if filme[3]:
                    detalhes += f" | Gênero: {filme[3]}"
                detalhes += f" | Nota: {filme[4]}/5"
                if filme[5]:
                    detalhes += f"\n💬 Comentários: {filme[5]}"
                
                detalhes += f"\n📅 Registrado em: {filme[6]}"
                self.label_detalhes.config(text=detalhes)

        except (ValueError, IndexError, sqlite3.Error):
            self.label_detalhes.config(text="Erro ao carregar detalhes do filme")

    def remover_filme(self):
        selecao = self.listbox_filmes.curselection()
        
        if not selecao:
            messagebox.showinfo("Seleção", "Selecione um filme para remover!")
            return

        if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este filme?"):
            texto_item = self.listbox_filmes.get(selecao[0])
           
            try:
                id_str = texto_item.split("]")[0].replace("[", "")
                id_filme = int(id_str)

                conexao = sqlite3.connect("filmes.db")
                cursor = conexao.cursor()
              
                cursor.execute("DELETE FROM filmes WHERE id = ?", (id_filme,))
                
                conexao.commit()
                conexao.close()

                self.atualizar_lista()
                self.label_detalhes.config(text="")
                messagebox.showinfo("Sucesso", "Filme removido!")

            except (ValueError, sqlite3.Error) as erro:
                messagebox.showerror("Erro", f"Falha ao remover: {erro}")

    def limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_ano.delete(0, tk.END)
        self.entry_genero.delete(0, tk.END)
        self.text_comentarios.delete("1.0", tk.END)
        self.nota.set("5")
        self.entry_titulo.focus()


# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    janela_principal = tk.Tk()
    
    app = CadastroFilmes(janela_principal)
   
    janela_principal.mainloop()