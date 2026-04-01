import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class SistemaConsultaFuncionarios:
    def __init__(self, janela_principal):
        self.janela_principal = janela_principal
        self.janela_principal.title("Sistema de Consulta de Funcionários")
        self.janela_principal.geometry("1000x700")
        self.caminho_banco_dados = "empresa.db"
        
        self.inicializar_banco_dados()
        self.criar_interface()
        self.carregar_funcionarios()
    
    def inicializar_banco_dados(self):
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    departamento TEXT NOT NULL,
                    salario REAL NOT NULL,
                    data_admissao TEXT NOT NULL
                )
            ''')
            
            cursor.execute('SELECT COUNT(*) FROM funcionarios')
            if cursor.fetchone()[0] == 0:
                funcionarios_iniciais = [
                    ('João Silva', 'Desenvolvedor', 'TI', 5000.00, '2022-01-15'),
                    ('Maria Santos', 'Analista', 'TI', 4500.00, '2021-06-20'),
                    ('Carlos Oliveira', 'Gerente', 'RH', 6000.00, '2020-03-10'),
                    ('Ana Costa', 'Especialista', 'TI', 5500.00, '2023-02-01'),
                    ('Pedro Martins', 'Assistente', 'Financeiro', 3000.00, '2023-08-15'),
                    ('Juliana Rocha', 'Coordenadora', 'RH', 5200.00, '2022-05-12'),
                    ('Roberto Alves', 'Desenvolvedor', 'TI', 5000.00, '2021-11-08'),
                    ('Beatriz Gomes', 'Analista', 'Financeiro', 4000.00, '2022-09-20'),
                    ('Lucas Ferreira', 'Estagiário', 'TI', 2000.00, '2024-01-10'),
                    ('Fernanda Lima', 'Diretora', 'RH', 8000.00, '2019-04-05')
                ]
                
                cursor.executemany('''
                    INSERT INTO funcionarios (nome, cargo, departamento, salario, data_admissao)
                    VALUES (?, ?, ?, ?, ?)
                ''', funcionarios_iniciais)
            
            conexao.commit()
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao inicializar banco de dados: {erro}")
    
    def criar_interface(self):
        frame_filtros = ttk.LabelFrame(self.janela_principal, text="Filtros", padding=10)
        frame_filtros.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(frame_filtros, text="Departamento:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.frame_departamentos = ttk.Frame(frame_filtros)
        self.frame_departamentos.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        scrollbar_departamentos = ttk.Scrollbar(self.frame_departamentos)
        scrollbar_departamentos.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_departamentos = tk.Listbox(
            self.frame_departamentos, 
            height=4, 
            width=20,
            yscrollcommand=scrollbar_departamentos.set
        )
        self.listbox_departamentos.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar_departamentos.config(command=self.listbox_departamentos.yview)
        self.listbox_departamentos.bind('<<ListboxSelect>>', lambda e: self.aplicar_filtros())
        
        ttk.Label(frame_filtros, text="Cargo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.frame_cargos = ttk.Frame(frame_filtros)
        self.frame_cargos.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        scrollbar_cargos = ttk.Scrollbar(self.frame_cargos)
        scrollbar_cargos.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_cargos = tk.Listbox(
            self.frame_cargos,
            height=4,
            width=20,
            yscrollcommand=scrollbar_cargos.set
        )
        self.listbox_cargos.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar_cargos.config(command=self.listbox_cargos.yview)
        self.listbox_cargos.bind('<<ListboxSelect>>', lambda e: self.aplicar_filtros())
        
        frame_salario = ttk.Frame(frame_filtros)
        frame_salario.grid(row=1, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(frame_salario, text="Salário Mínimo:").pack(side=tk.LEFT, padx=5)
        self.entrada_salario_minimo = ttk.Entry(frame_salario, width=10)
        self.entrada_salario_minimo.pack(side=tk.LEFT, padx=5)
        self.entrada_salario_minimo.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        ttk.Label(frame_salario, text="Salário Máximo:").pack(side=tk.LEFT, padx=5)
        self.entrada_salario_maximo = ttk.Entry(frame_salario, width=10)
        self.entrada_salario_maximo.pack(side=tk.LEFT, padx=5)
        self.entrada_salario_maximo.bind('<KeyRelease>', lambda e: self.aplicar_filtros())
        
        frame_botoes_ordenacao = ttk.LabelFrame(self.janela_principal, text="Ordenação", padding=10)
        frame_botoes_ordenacao.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(frame_botoes_ordenacao, text="Ordenar por Nome", command=self.ordenar_por_nome).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_ordenacao, text="Ordenar por Cargo", command=self.ordenar_por_cargo).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_ordenacao, text="Ordenar por Salário", command=self.ordenar_por_salario).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_ordenacao, text="Limpar Filtros", command=self.limpar_filtros).pack(side=tk.LEFT, padx=5)
        
        frame_tabela = ttk.LabelFrame(self.janela_principal, text="Funcionários", padding=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar_tabela = ttk.Scrollbar(frame_tabela)
        scrollbar_tabela.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_funcionarios = tk.Listbox(
            frame_tabela,
            font=("Courier", 9),
            yscrollcommand=scrollbar_tabela.set
        )
        self.listbox_funcionarios.pack(fill=tk.BOTH, expand=True)
        scrollbar_tabela.config(command=self.listbox_funcionarios.yview)
        self.listbox_funcionarios.bind('<<ListboxSelect>>', self.mostrar_detalhes)
        
        frame_detalhes = ttk.LabelFrame(self.janela_principal, text="Detalhes do Funcionário", padding=10)
        frame_detalhes.pack(fill=tk.X, padx=10, pady=10)
        
        self.texto_detalhes = tk.Text(frame_detalhes, height=4, width=80)
        self.texto_detalhes.pack(fill=tk.BOTH)
        
        frame_estatisticas = ttk.LabelFrame(self.janela_principal, text="Estatísticas", padding=10)
        frame_estatisticas.pack(fill=tk.X, padx=10, pady=10)
        
        self.label_estatisticas = ttk.Label(frame_estatisticas, text="")
        self.label_estatisticas.pack(fill=tk.X)
        
        self.ordem_atual = None
        self.funcionarios_exibidos = []
    
    def carregar_funcionarios(self):
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            
            cursor.execute('SELECT DISTINCT departamento FROM funcionarios ORDER BY departamento')
            departamentos = cursor.fetchall()
            self.listbox_departamentos.delete(0, tk.END)
            for departamento in departamentos:
                self.listbox_departamentos.insert(tk.END, departamento[0])
            
            cursor.execute('SELECT DISTINCT cargo FROM funcionarios ORDER BY cargo')
            cargos = cursor.fetchall()
            self.listbox_cargos.delete(0, tk.END)
            for cargo in cargos:
                self.listbox_cargos.insert(tk.END, cargo[0])
            
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao carregar filtros: {erro}")
    
    def aplicar_filtros(self):
        departamentos_selecionados = [self.listbox_departamentos.get(i) for i in self.listbox_departamentos.curselection()]
        cargos_selecionados = [self.listbox_cargos.get(i) for i in self.listbox_cargos.curselection()]
        
        try:
            salario_minimo = float(self.entrada_salario_minimo.get()) if self.entrada_salario_minimo.get() else 0
        except ValueError:
            salario_minimo = 0
        
        try:
            salario_maximo = float(self.entrada_salario_maximo.get()) if self.entrada_salario_maximo.get() else float('inf')
        except ValueError:
            salario_maximo = float('inf')
        
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            
            consulta = 'SELECT * FROM funcionarios WHERE 1=1'
            parametros = []
            
            if departamentos_selecionados:
                placeholders = ','.join(['?' for _ in departamentos_selecionados])
                consulta += f' AND departamento IN ({placeholders})'
                parametros.extend(departamentos_selecionados)
            
            if cargos_selecionados:
                placeholders = ','.join(['?' for _ in cargos_selecionados])
                consulta += f' AND cargo IN ({placeholders})'
                parametros.extend(cargos_selecionados)
            
            if salario_minimo > 0 or salario_maximo != float('inf'):
                consulta += ' AND salario BETWEEN ? AND ?'
                parametros.extend([salario_minimo, salario_maximo])
            
            if self.ordem_atual:
                consulta += f' ORDER BY {self.ordem_atual}'
            else:
                consulta += ' ORDER BY nome'
            
            cursor.execute(consulta, parametros)
            funcionarios = cursor.fetchall()
            
            self.listbox_funcionarios.delete(0, tk.END)
            self.funcionarios_exibidos = funcionarios
            for funcionario in funcionarios:
                linha = f"{funcionario[1]:<20} {funcionario[3]:<15} {funcionario[2]:<15} R$ {funcionario[4]:>10,.2f}"
                self.listbox_funcionarios.insert(tk.END, linha)
            
            self.atualizar_estatisticas()
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao aplicar filtros: {erro}")
    
    def ordenar_por_nome(self):
        self.ordem_atual = 'nome'
        self.aplicar_filtros()
    
    def ordenar_por_cargo(self):
        self.ordem_atual = 'cargo'
        self.aplicar_filtros()
    
    def ordenar_por_salario(self):
        self.ordem_atual = 'salario DESC'
        self.aplicar_filtros()
    
    def limpar_filtros(self):
        self.listbox_departamentos.selection_clear(0, tk.END)
        self.listbox_cargos.selection_clear(0, tk.END)
        self.entrada_salario_minimo.delete(0, tk.END)
        self.entrada_salario_maximo.delete(0, tk.END)
        self.ordem_atual = None
        self.aplicar_filtros()
    
    def mostrar_detalhes(self, evento):
        selecao = self.listbox_funcionarios.curselection()
        if selecao:
            indice = selecao[0]
            if indice < len(self.funcionarios_exibidos):
                funcionario = self.funcionarios_exibidos[indice]
                detalhes = f"""
ID: {funcionario[0]}
Nome: {funcionario[1]}
Cargo: {funcionario[3]}
Departamento: {funcionario[2]}
Salário: R$ {funcionario[4]:,.2f}
Data de Admissão: {funcionario[5]}
"""
                self.texto_detalhes.delete(1.0, tk.END)
                self.texto_detalhes.insert(1.0, detalhes)
    
    def atualizar_estatisticas(self):
        try:
            conexao = sqlite3.connect(self.caminho_banco_dados)
            cursor = conexao.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM funcionarios')
            total_funcionarios = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(salario) FROM funcionarios')
            folha_salarial = cursor.fetchone()[0] or 0
            
            cursor.execute('''
                SELECT departamento, AVG(salario)
                FROM funcionarios
                GROUP BY departamento
                ORDER BY departamento
            ''')
            media_por_departamento = cursor.fetchall()
            
            texto_estatisticas = f"Total de Funcionários: {total_funcionarios} | Folha Salarial: R$ {folha_salarial:,.2f} | "
            texto_estatisticas += "Média por Departamento: "
            
            for departamento, media in media_por_departamento:
                texto_estatisticas += f"{departamento}: R$ {media:,.2f} | "
            
            self.label_estatisticas.config(text=texto_estatisticas)
            conexao.close()
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao calcular estatísticas: {erro}")

if __name__ == "__main__":
    janela = tk.Tk()
    aplicacao = SistemaConsultaFuncionarios(janela)
    janela.mainloop()