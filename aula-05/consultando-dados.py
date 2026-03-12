import sqlite3

conexao = sqlite3.connect("escola.db")
cursor = conexao.cursor()

# Consultar todos os alunos
cursor.execute("SELECT * FROM alunos")
resultados = cursor.fetchall()

print("=" * 50)
print("LISTA DE ALUNOS CADASTRADOS")
print("=" * 50)

for aluno in resultados:
    print(f"ID: {aluno[0]} | Nome: {aluno[1]} | Idade: {aluno[2]} | Curso: {aluno[3]}")

print("=" * 50)
print(f"Total de alunos: {len(resultados)}")

conexao.close()