import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Conversor de Temperatura")
janela.geometry("400x360")
janela.configure(bg="white")
janela.resizable(False, False)

menubar = tk.Menu(janela)
menu_arquivo = tk.Menu(menubar, tearoff=0)
menu_arquivo.add_command(label="Sair", command=janela.quit)
menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_ajuda = tk.Menu(menubar, tearoff=0)
menu_ajuda.add_command(label="Sobre", command=lambda: messagebox.showinfo("Sobre", "Conversor de Temperatura\nDesenvolvido em Python com Tkinter"))
menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
janela.config(menu=menubar)

tk.Label(janela, text="Conversor de Temperatura", font=("Arial", 14, "bold"), bg="lightblue", pady=8).pack(fill="x")

frame_entrada = tk.Frame(janela, bg="white", pady=8)
frame_entrada.pack()

tk.Label(frame_entrada, text="Temperatura:", font=("Arial", 10), bg="white").grid(row=0, column=0, padx=10, sticky="w")
entry_valor = tk.Entry(frame_entrada, font=("Arial", 10), width=20, relief="solid", bd=1)
entry_valor.grid(row=0, column=1, padx=10)

frame_orig = tk.LabelFrame(janela, text="De (origem)", font=("Arial", 10, "bold"), bg="white", padx=10, pady=6)
frame_orig.pack(fill="x", padx=20, pady=4)

origem = tk.StringVar(value="Celsius")
tk.Radiobutton(frame_orig, text="Celsius",    variable=origem, value="Celsius", bg="white", font=("Arial", 10)).pack(side="left", padx=15)
tk.Radiobutton(frame_orig, text="Fahrenheit", variable=origem, value="Fahrenheit", bg="white", font=("Arial", 10)).pack(side="left", padx=15)

frame_dest = tk.LabelFrame(janela, text="Para (destino)", font=("Arial", 10, "bold"), bg="white", padx=10, pady=6)
frame_dest.pack(fill="x", padx=20, pady=4)

destino = tk.StringVar(value="Fahrenheit")
tk.Radiobutton(frame_dest, text="Celsius",    variable=destino, value="Celsius", bg="white", font=("Arial", 10)).pack(side="left", padx=15)
tk.Radiobutton(frame_dest, text="Fahrenheit", variable=destino, value="Fahrenheit", bg="white", font=("Arial", 10)).pack(side="left", padx=15)

label_resultado = tk.Label(janela, text="", font=("Arial", 11, "bold"), bg="lightyellow", pady=8, relief="flat")
label_resultado.pack(fill="x", padx=20, pady=4)

def converter():
    if origem.get() == destino.get():
        messagebox.showerror("Erro", "Origem e destino não podem ser iguais!")
        return
    try:
        valor = float(entry_valor.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Informe um valor numérico válido.")
        return
    if origem.get() == "Celsius":
        resultado = (valor * 9/5) + 32
        label_resultado.config(text=f"{valor:.2f} °C = {resultado:.2f} °F")
    else:
        resultado = (valor - 32) * 5/9
        label_resultado.config(text=f"{valor:.2f} °F = {resultado:.2f} °C")

def limpar():
    entry_valor.delete(0, tk.END)
    origem.set("Celsius")
    destino.set("Fahrenheit")
    label_resultado.config(text="")

frame_btn = tk.Frame(janela, bg="white")
frame_btn.pack(pady=6)

tk.Button(frame_btn, text="Converter", font=("Arial", 10, "bold"), bg="lightblue", fg="black", padx=12, pady=4, command=converter).pack(side="left", padx=8)
tk.Button(frame_btn, text="Limpar", font=("Arial", 10, "bold"), bg="lightyellow", fg="black", padx=12, pady=4, command=limpar).pack(side="left", padx=8)

janela.mainloop()