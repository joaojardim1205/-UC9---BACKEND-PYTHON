import sqlite3

# Conecta (se o arquivo .db não existir, ele será criado)
conexao = sqlite3.connect("escola.db")
cursor = conexao.cursor()

# Criando uma tabela de alunos
cursor.execute("""
    CREATE TABLE alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        curso TEXT
    )
""")

conexao.commit()
conexao.close()

print("Banco de dados 'escola.db' criado com sucesso!")
print("Tabela 'alunos' criada dentro do DB")