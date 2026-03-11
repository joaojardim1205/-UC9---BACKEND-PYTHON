import tkinter as tk

janela = tk.Tk()
janela.title("Sistema de Cadastro")
janela.geometry("400x300")
janela.configure(bg="white")
janela.resizable(False, False)

tk.Label(janela, text="Cadastro de Pessoas", font=("Arial", 14, "bold"),
         bg="lightblue", pady=8).pack(fill="x")

frame = tk.Frame(janela, bg="white", pady=10)
frame.pack()

tk.Label(frame, text="Nome:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=10, pady=6, sticky="w")
entry_nome = tk.Entry(frame, font=("Arial", 10), width=25, relief="solid", bd=1)
entry_nome.grid(row=0, column=1, padx=10, pady=6)

tk.Label(frame, text="Idade:", font=("Arial", 10), bg="white").grid(row=1, column=0, padx=10, pady=6, sticky="w")
entry_idade = tk.Entry(frame, font=("Arial", 10), width=25, relief="solid", bd=1)
entry_idade.grid(row=1, column=1, padx=10, pady=6)

label_resultado = tk.Label(janela, text="", font=("Arial", 10), bg="lightyellow", pady=8, relief="flat")
label_resultado.pack(fill="x", padx=20)

def mostrar():
    label_resultado.config(text=f"Nome: {entry_nome.get()} - Idade: {entry_idade.get()} anos")

def limpar():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    label_resultado.config(text="")

frame_btn = tk.Frame(janela, bg="white")
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Mostrar Dados", font=("Arial", 10, "bold"), bg="lightblue", fg="black", padx=12, pady=4, command=mostrar).pack(side="left", padx=8)
tk.Button(frame_btn, text="Limpar", font=("Arial", 10, "bold"), bg="lightyellow", fg="black", padx=12, pady=4, command=limpar).pack(side="left", padx=8)

janela.mainloop()