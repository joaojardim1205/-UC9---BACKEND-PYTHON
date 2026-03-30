import sqlite3

conexao = sqlite3.connect('clientes.db')
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        idade INTEGER,
        cidade TEXT
    )
""")

clientes_exemplo = [
    ("João Silva", "joao@gmail.com", 28, "São Paulo"),
    ("Maria Oliveira", "maria@gmail.com", 21, "Rio de Janeiro"),
    ("Carlos Santos", "carlos@gmail.com", 45, "Belo Horizonte"),
    ("Arthur Golçalves", "arthur@gmail.com", 18, "São Paulo"),
    ("Ana Silva", "ana@gmail.com", 30, "São Paulo")
]

cursor.executemany("""
    INSERT OR IGNORE INTO clientes (nome, email, idade, cidade) 
    VALUES (?, ?, ?, ?)
""", clientes_exemplo)

conexao.commit()

# Exemplo 1 (SELECT simples)
cursor.execute("SELECT * FROM clientes")
todos_clientes = cursor.fetchall()

print("Todos os clientes:")
for cliente in todos_clientes:
    print(cliente)

# Exemplo 2 (SELECT com campos específicos)
cursor.execute("SELECT nome, email FROM clientes")
nomes_emails = cursor.fetchall()
print("\nNomes e emails:")
for nome, email in nomes_emails:
    print(f"Nome: {nome}, Email: {email}")

# Exemplo 3 (SELECT com condição)
cursor.execute("SELECT * FROM clientes WHERE cidade = 'São Paulo'")
clientes_sp = cursor.fetchall()
print(f"\nClientes de São Paulo: {len(clientes_sp)} encontrados")

# Exemplo 4 (SELECT com ORDER BY)
cursor.execute("SELECT nome, idade FROM clientes ORDER BY idade DESC")
clientes_ordenados = cursor.fetchall()
print("\nClientes ordenados por idade:")
for nome, idade in clientes_ordenados:
    print(f"{nome}: {idade} anos")

# Exemplo 5 (SELECT com ordenação)
cursor.execute("SELECT nome FROM clientes LIMIT 3")
primeiros_3 = cursor.fetchall() 
print("\nPrimeiros 3 clientes:")
for nome in primeiros_3:
    print(f"Nome: {nome[0]}")

# Exemplo 6 (SELECT com COUNT)
cursor.execute("SELECT COUNT(*) FROM clientes")
total = cursor.fetchone()[0] # fecthone() retorna uma tupla com um elemento
print(f"\nTotal de clientes: {total}")

# Exemplo 7 (SELECT com LIKE)
cursor.execute("SELECT nome FROM clientes WHERE nome LIKE '%silva%'")
clientes_silva = cursor.fetchall()
print(f"\nClientes com nome 'silva':")
for nome in clientes_silva:
    print(cliente[0])

conexao.close()
