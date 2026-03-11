import tkinter as tk

janela = tk.Tk()
janela.title("Contador de Cliques")
janela.geometry("300x200")

contador = 0

label_contador = tk.Label(janela, text="0", font=("Arial", 24), fg="black")
label_contador.pack(pady=10)

label_notificacao = tk.Label(janela, text="", font=("Arial", 10))
label_notificacao.pack()

def atualizar(mensagem):
    cor = "green" if contador > 0 else ("red" if contador < 0 else "black")
    label_contador.config(text=str(contador), fg=cor)
    label_notificacao.config(text=mensagem)

def incrementar():
    global contador
    contador += 1
    atualizar("Incrementou")

def decrementar():
    global contador
    if contador > 0:
        contador -= 1
        atualizar("Decrementou")

def reset():
    global contador
    contador = 0
    atualizar("Reset")

tk.Button(janela, text="Clique aqui", command=incrementar).pack(pady=2)
tk.Button(janela, text="Diminuir", command=decrementar).pack(pady=2)
tk.Button(janela, text="Reset", command=reset).pack(pady=2)

janela.mainloop()   