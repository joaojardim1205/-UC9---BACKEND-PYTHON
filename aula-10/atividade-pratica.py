import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SistemaConsultaAlunos:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title("Sistema de Consulta de Alunos")
        self.janela_principal.geometry("700x600")

        self.caminho_banco_dados = "escola.db"
        self.lista_alunos_filtrados = []
        self.curso_selecionado = tk.StringVar(value="Todos")

        self.inicializar_banco_dados()
        self.criar_interface_usuario()
        self.carregar_todos_alunos()

    def inicializar_banco_dados(self):
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alunos(
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    idade INTEGER,
                    curso TEXT,
                    nota_media REAL
                )''')

            cursor.execute("SELECT COUNT(*) FROM alunos")
            if cursor.fetchone()[0] == 0:
                dados_exemplo = [
                    ("João Silva", 20, "Python", 8.5),
                    ("Maria Santos", 21, "Java", 9.0),
                    ("Pedro Costa", 19, "Banco de Dados", 7.8),
                    ("Ana Oliveira", 22, "Python", 8.2),
                ]
                cursor.executemany("INSERT INTO alunos (nome, idade, curso, nota_media) VALUES (?, ?, ?, ?)", dados_exemplo)

            conexao.commit()
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao inicializar banco: {erro}")

    def criar_interface_usuario(self):
        quadro_filtros = ttk.LabelFrame(self.janela_principal, text="Filtros e Busca", padding=10)
        quadro_filtros.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(quadro_filtros, text="Buscar por nome:").grid(row=0, column=0, sticky=tk.W)
        self.entrada_busca_nome = ttk.Entry(quadro_filtros, width=30)
        self.entrada_busca_nome.grid(row=0, column=1, padx=5)
        self.entrada_busca_nome.bind("<KeyRelease>", lambda evento: self.filtrar_alunos())

        ttk.Label(quadro_filtros, text="Curso:").grid(row=1, column=0, sticky=tk.W, pady=10)
        lista_cursos = ["Todos", "Python", "Java", "Banco de Dados"]

        for indice, curso in enumerate(lista_cursos):
            ttk.Radiobutton(quadro_filtros, text=curso, variable=self.curso_selecionado,
                           value=curso, command=self.filtrar_alunos).grid(row=1, column=indice + 1, padx=5)

        ttk.Button(quadro_filtros, text="Todos os Alunos", command=self.carregar_todos_alunos).grid(row=2, column=0, pady=10)

        quadro_lista = ttk.LabelFrame(self.janela_principal, text="Alunos Cadastrados", padding=10)
        quadro_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        barra_rolagem = ttk.Scrollbar(quadro_lista)
        barra_rolagem.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox_alunos = tk.Listbox(quadro_lista, yscrollcommand=barra_rolagem.set, height=10)
        self.listbox_alunos.pack(fill=tk.BOTH, expand=True)
        self.listbox_alunos.bind("<<ListboxSelect>>", self.mostrar_detalhes_aluno)
        barra_rolagem.config(command=self.listbox_alunos.yview)

        quadro_detalhes = ttk.LabelFrame(self.janela_principal, text="Detalhes do Aluno", padding=10)
        quadro_detalhes.pack(fill=tk.X, padx=10, pady=10)

        self.label_detalhes_aluno = ttk.Label(quadro_detalhes, text="Selecione um aluno para ver detalhes",
                                             wraplength=600, justify=tk.LEFT)
        self.label_detalhes_aluno.pack()

        self.status_texto = tk.StringVar(value="Total de alunos: 0")
        barra_status = ttk.Label(self.janela_principal, textvariable=self.status_texto, relief=tk.SUNKEN)
        barra_status.pack(fill=tk.X, side=tk.BOTTOM)

    def carregar_todos_alunos(self):
        self.entrada_busca_nome.delete(0, tk.END)
        self.curso_selecionado.set("Todos")
        self.filtrar_alunos()

    def filtrar_alunos(self):
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()

            texto_busca = self.entrada_busca_nome.get().lower()
            curso_filtro = self.curso_selecionado.get()

            consulta = "SELECT id, nome, curso, nota_media FROM alunos WHERE nome LIKE ?"
            parametros = [f"%{texto_busca}%"]

            if curso_filtro != "Todos":
                consulta += " AND curso = ?"
                parametros.append(curso_filtro)

            cursor.execute(consulta, parametros)
            self.lista_alunos_filtrados = cursor.fetchall()
            conexao.close()

            self.atualizar_listbox()
        except sqlite3.Error as erro:
            self.status_texto.set(f"Erro: {erro}")

    def atualizar_listbox(self):
        self.listbox_alunos.delete(0, tk.END)
        for aluno in self.lista_alunos_filtrados:
            texto_exibicao = f"{aluno[1]} - {aluno[2]} - Média: {aluno[3]}"
            self.listbox_alunos.insert(tk.END, texto_exibicao)

        self.status_texto.set(f"Total de alunos: {len(self.lista_alunos_filtrados)}")
        self.label_detalhes_aluno.config(text="Selecione um aluno para ver detalhes")

    def mostrar_detalhes_aluno(self, evento):
        try:
            indice_selecionado = self.listbox_alunos.curselection()[0]
            aluno_id = self.lista_alunos_filtrados[indice_selecionado][0]

            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
            aluno = cursor.fetchone()
            conexao.close()

            if aluno:
                texto_detalhes = (
                    f"ID: {aluno[0]}\n"
                    f"Nome: {aluno[1]}\n"
                    f"Idade: {aluno[2]}\n"
                    f"Curso: {aluno[3]}\n"
                    f"Nota Média: {aluno[4]}"
                )
                self.label_detalhes_aluno.config(text=texto_detalhes)
        except (IndexError, sqlite3.Error) as erro:
            self.status_texto.set(f"Erro ao carregar detalhes: {erro}")

if __name__ == "__main__":
    janela = tk.Tk()
    aplicacao = SistemaConsultaAlunos(janela)
    janela.mainloop()
