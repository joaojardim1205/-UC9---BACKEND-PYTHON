import sqlite3

conexao = sqlite3.connect("escola.db")
cursor = conexao.cursor()

# Inserindo um aluno
cursor.execute("""
    INSERT INTO alunos (nome, idade, curso)
    VALUES (?, ?, ?)
""", ("Maria Silva", 20, "Python"))

# Inserindo vários alunos
alunos = [
    ("João Santos", 22, "Java"),
    ("Ana Oliveira", 19, "Python"),
    ("Carlos Lima", 21, "Banco de Dados")
]

cursor.executemany("""
    INSERT INTO alunos (nome, idade, curso)
    VALUES (?, ?, ?)
""", alunos)

conexao.commit()
conexao.close()

print("Dados inseridos com sucesso!")