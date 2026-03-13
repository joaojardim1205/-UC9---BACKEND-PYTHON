# SISTEMA DE CADASTRO DE CLIENTES

# PASSO 1: Importar as bibliotecas necessárias
import tkinter as tk
from tkinter import messagebox
import sqlite3

# CLASSSE DO SISTEMA: orgnaiza todo o código
class SistemaCadastro:
    def __init__(self, janela):
        # Guarda a referência da janela principal
        self.janela = janela
        self.janela.title("Sistema de Cadastro de Clientes")
        self.janela.geometry("500x400")

        # Chama o método que cria o DB
        self.criar_banco_dados()
        
        # Chama o método que cria a interface
        self.criar_interface()

        # Chama o método que atualiza a lista de clientes
        self.listar_clientes()

    # MÉTODO 1: criar o DB e a tabela
    def criar_banco_dados(self):
        try:
            # Conecta DB (cria o arquivo se não existir)
            self.conexao = sqlite3.connect('clientes.db')
            self.cursor = self.conexao.cursor()

            # Cria a tabela de clientes (se não existir)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    telefone TEXT,
                    data_cadastro DATE DEFAULT CURRENT_DATE
                )
            """)
            # Salva as alterações
            self.conexao.commit()
            self.conexao.close()

            print("Banco de dados criado/verificado com sucesso!")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao criar/verificar DB: {erro}")