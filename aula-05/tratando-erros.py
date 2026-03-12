import sqlite3

try:
    conexao = sqlite3.connect("escola.db")
    cursor = conexao.cursor()

    # Tentar criar tabela (se já existir, não dá erro)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOENCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        curso TEXT
    )
""")
    
    conexao.commit()
    print("Operação realizada com sucesso!")

except sqlite3.Error as erro:
    print(f"Erro no banco de dados: {erro}")

finally:
    if conexao:
        conexao.close()
        print("Conexão fechada")
    