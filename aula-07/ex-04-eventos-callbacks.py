import tkinter as tk

def evento_clique():
    print("Botão clicado!")

def evento_tecla(event):
    print(f"Tecla pressionada: {event.char}")

def evento_enter(event):
    print("Mouse entrou no botão")

def evento_leave(event):
    print("Mouse saiu do botão")

def evento_foco_entrada(event):
    print("Campo ganhou foco")

def evento_foco_saida(event):
    print("Campo perdeu foco")
    valor = entry.get()
    print(f"Valor digitado: {valor}")

janela = tk.Tk()
janela.title("Exemplo de Eventos")
janela.geometry("400x300")

# Evento de clique em botão
btn = tk.Button(janela, text="Clique aqui")
btn.pack(pady=10)

btn.bind("<Button-1>", lambda e: evento_clique())  # <Button-1> = clique esquerdo

# Eventos de mouse
btn2 = tk.Button(janela, text="Passe o Mouse")
btn2.pack(pady=10)
btn2.bind("<Enter>", evento_enter) # Mouse entrou na área
btn2.bind("<Leave>", evento_leave) # Mouse saiu da área

# Eventos de teclado em Entry
entry = tk.Entry(janela, width=30)
entry.pack(pady=10)
entry.bind("<Key>", evento_tecla) # Qualquer tecla pressionada
entry.bind("<FocusIn>", evento_foco_entrada) # Ganhou foco
entry.bind("<FocusOut>", evento_foco_saida) # Perdeu foco

# Evento de tecla Enter
entry.bind("<Return>", lambda e: print("Enter pressionado!"))

janela.mainloop()