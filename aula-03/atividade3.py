import tkinter as tk
from tkinter import messagebox

janela = tk.Tk()
janela.title("Calculadora de IMC")
janela.geometry("400x380")
janela.configure(bg="white")
janela.resizable(False, False)

tk.Label(janela, text="Calculadora de IMC", font=("Arial", 14, "bold"), bg="lightblue", pady=8).pack(fill="x")

frame = tk.Frame(janela, bg="white", pady=10)
frame.pack()

def campo(texto, row):
    tk.Label(frame, text=texto, font=("Arial", 10), bg="white", width=12, anchor="w").grid(row=row, column=0, padx=10, pady=6)
    e = tk.Entry(frame, font=("Arial", 10), width=22, relief="solid", bd=1)
    e.grid(row=row, column=1, padx=10, pady=6)
    return e

entry_nome  = campo("Nome:", 0)
entry_peso  = campo("Peso (kg):", 1)
entry_altura = campo("Altura (m):", 2)

label_resultado = tk.Label(janela, text="", font=("Arial", 10), bg="lightyellow", pady=10, wraplength=360, relief="flat")
label_resultado.pack(fill="x", padx=20, pady=4)

label_class = tk.Label(janela, text="", font=("Arial", 11, "bold"), bg="lightblue", pady=8, relief="flat")
label_class.pack(fill="x", padx=20, pady=2)

def classificar(imc):
    if imc < 18.5:   return "Abaixo do peso"
    elif imc < 25:   return "Peso normal"
    elif imc < 30:   return "Sobrepeso"
    elif imc < 35:   return "Obesidade grau I"
    elif imc < 40:   return "Obesidade grau II"
    else:            return "Obesidade grau III"

def calcular():
    try:
        peso   = float(entry_peso.get().replace(",", "."))
        altura = float(entry_altura.get().replace(",", "."))
        if peso <= 0 or altura <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erro", "Informe peso e altura como números positivos.")
        return
    imc = peso / (altura ** 2)
    nome = entry_nome.get() or "Você"
    label_resultado.config(text=f"{nome} — IMC: {imc:.2f}")
    label_class.config(text=classificar(imc))

def limpar():
    for e in (entry_nome, entry_peso, entry_altura):
        e.delete(0, tk.END)
    label_resultado.config(text="")
    label_class.config(text="")

frame_btn = tk.Frame(janela, bg="white")
frame_btn.pack(pady=8)

tk.Button(frame_btn, text="Calcular IMC", font=("Arial", 10, "bold"), bg="lightblue", fg="black", padx=12, pady=4, command=calcular).pack(side="left", padx=8)
tk.Button(frame_btn, text="Limpar", font=("Arial", 10, "bold"), bg="lightyellow", fg="black", padx=12, pady=4, command=limpar).pack(side="left", padx=8)

janela.mainloop()