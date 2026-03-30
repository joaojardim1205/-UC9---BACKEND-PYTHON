import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class SistemaConsultaProdutos:
    """
    Classe que gerencia o sistema de consulta de produtos.
    Demonstra SELECT simples, preenchimento de Listbox e tratamento de exceções
    """

    def __init__(self, janela):
        """
        Construtor da classe.
        Inicializa a janela, cria o banco de dados e a interface
        """

        self.janela = janela
        self.janela.title("Sistema de Consulta de Produtos")
        self.janela.geometry("800x600")

        # Inicializar variaveis de controle
        self.todos_produtos = [] 

        self.label_status = None

        # Criar interface grafica
        self.criar_interface()

        # Criar banco de dados e tabela
        self.criar_banco_dados()

        # Carregar produtos iniciais
        self.carregar_todos_produtos()

        # Inserir dados de exemplo
        self.inserir_dados_exemplo()

    def criar_banco_dados(self):
        """
        Cria o banco de dados e a tabela de produtos
        Inclue tratamento de exceções oara possiveis erros
        """

        try:
            self.conexao = sqlite3.connect('produtos_consulta.db')
            self.cursor = self.conexao.cursor()

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    categoria TEXT,
                    preco REAL NOT NULL,
                    estoque INTEGER,
                    data_cadastro TEXT
                )
            ''')
            self.conexao.commit()
            self.conexao.close()

            self.atualizar_status("Banco de dados criado/verificado com sucesso!.")
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro de banco de dados", f"falha ao criar banco de dados:\n{erro}")
            self.atualizar_status("Erro ao criar banco de dados.")
