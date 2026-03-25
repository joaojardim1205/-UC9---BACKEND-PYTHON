import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class CadastroTarefas:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Gerenciador de Tarefas")
        self.janela.geometry("600x500")

        self.criar_banco()
        self.criar_interface()
        self.listar_tarefas()


    def criar_banco(self):   
        self.conexao = sqlite3.connect("tarefas.db")
        self.cursor = self.conexao.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                prioridade TEXT,
                data_criacao TEXT
            )
        """)
        self.conexao.commit()
        self.conexao.close()

    def criar_interface(self):
        # Título
        tk.Label (
            self.janela, 
            text="GERENCIADOR DE TAREFAS",
            font=("Arial", 14, "bold"),
            fg="darkblue"
        ).pack(pady=10)

        # Frame de entrada (Entry)
        frame_entry = tk.Frame(self.janela)
        frame_entry.pack(pady=5)

        tk.Label(frame_entry, text="Título:", font=("Arial", 10)).pack(side="left")

        self.entry_titulo = tk.Entry(frame_entry, width=40, font=("Arial", 10))
        self.entry_titulo.pack(side="left", padx=5)

        # Frame de prioridade (Radiobutton)
        frame_prioridade = tk.Frame(self.janela)
        frame_prioridade.pack(pady=5)

        tk.Label(frame_prioridade, text="Prioridade:", font=("Arial", 10)).pack(side="left")

        self.prioridade = tk.StringVar(value="Média")
        prioridade = ["Alta", "Média", "Baixa"]

        for p in prioridade:
            tk.Radiobutton(
                frame_prioridade, 
                text=p, 
                variable=self.prioridade, 
                value=p,
            ).pack(side="left", padx=5)

        # Área de texto (Text) para descrição
        tk.Label(self.janela, text="Descrição:", font=("Arial", 10)).pack(pady=5)
        self.text_descricao = tk.Text(
            self.janela, 
            height=4, 
            width=50, 
            font=("Arial", 10)
        )
        self.text_descricao.pack(pady=5)

        # Frame de botões
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        tk.Button(
            frame_botoes,
            text="Adicionar Tarefa",
            command=self.adicionar_tarefa,
            bg="green",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botoes,
            text="Limpar",
            command=self.limpar_campos,
            bg="orange",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side="left", padx=5)

        # Listbox para exibir tarefas
        tk.Label(self.janela, text="Tarefas Cadastradas:", font=("Arial", 10)).pack()

        frame_lista = tk.Frame(self.janela)
        frame_lista.pack(pady=5, fill="both", expand=True, padx=10)

        self.listbox_tarefas = tk.Listbox(
            frame_lista, 
            height=10,
            font=("Arial", 10),
            selectmode="single"
        )
        self.listbox_tarefas.pack(side="left", fill="both", expand=True)

        # Scrollbar para a Listbox
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_tarefas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_tarefas.yview)

        # Bind de seleção na Listbox
        self.listbox_tarefas.bind("<<ListboxSelect>>", self.mostrar_detalhes)

        # Label para mostrar detalhes da tarefa selecionada
        self.label_detalhes = tk.Label(
            self.janela, 
            text="", 
            font=("Arial", 9), 
            justify="left",
            fg="gray"
        )
        self.label_detalhes.pack(pady=5)

    def adicionar_tarefa(self):
        # Pegar dados da interface
        titulo = self.entry_titulo.get().strip()
        descricao = self.text_descricao.get("1.0", "end-1c").strip()
        prioridade = self.prioridade.get()
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Validação
        if not titulo:
            messagebox.showwarning("Aviso", "O título é obrigatório!")
            return
        
        # Inserir no banco
        try:
            conexao = sqlite3.connect("tarefas.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO tarefas (titulo, descricao, prioridade, data_criacao)
                VALUES (?, ?, ?, ?)
            """, (titulo, descricao, prioridade, data_atual))
            conexao.commit()
            conexao.close()

            messagebox.showinfo("Sucesso", "Tarefa adicionada!")
            self.limpar_campos()
            self.listar_tarefas()

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao salvar: {erro}")

    def listar_tarefas(self):
        # Limpar Listbox
        self.listbox_tarefas.delete(0, tk.END)

        try:
            conexao = sqlite3.connect("tarefas.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, titulo, prioridade FROM tarefas ORDER BY data_criacao DESC")
            tarefas = cursor.fetchall()
            conexao.close()

            for tarefa in tarefas:
                # Formatar: [ID] Título (Prioridade)
                texto = f"[{tarefa[0]}] {tarefa[1]} ({tarefa[2]})"
                self.listbox_tarefas.insert(tk.END, texto)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao listar: {erro}")

    def mostrar_detalhes(self, event):
        selecao = self.listbox_tarefas.curselection()
        if not selecao:
            return
        
        # Pegar o texto selecionado
        texto_item = self.listbox_tarefas.get(selecao[0])

        # Extrair o ID do texto (formato: [ID] Título (Prioridade))

        id_str = texto_item.split("]")[0].replace("[", "")

        try:
            id_tarefa = int(id_str)

            conexao = sqlite3.connect("tarefas.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,))
            tarefa = cursor.fetchone()
            conexao.close()

            if tarefa:
                detalhes = f"ID: {tarefa[0]}\n"
                detalhes += f"Título: {tarefa[1]}\n"
                detalhes += f"Descrição: {tarefa[2]}\n"
                detalhes += f"Prioridade: {tarefa[3]}\n"
                detalhes += f"Criada em: {tarefa[4]}\n"

                self.label_detalhes.config(text=detalhes)
        
        except (ValueError, sqlite3.Error):
            self.label_detalhes.config(text="Erro ao carregar detalhes.")

    def limpar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.text_descricao.delete("1.0", tk.END)
        self.prioridade.set("Média")
        self.label_detalhes.config(text="")
        self.entry_titulo.focus()

# Executar
janela = tk.Tk()
app = CadastroTarefas(janela)
janela.mainloop()