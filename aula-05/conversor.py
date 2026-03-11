import tkinter as tk

janela = tk.Tk()
janela.title("Conversor de Medidas")
janela.geometry("350x300")

fatores = {"cm": 1, "m": 100, "km": 100000}

origem = tk.StringVar(value="cm")
destino = tk.StringVar(value="m")

tk.Label(janela, text="Valor:").pack(pady=(10, 0))
entry_valor = tk.Entry(janela, justify="center")
entry_valor.pack()

tk.Label(janela, text="De:").pack(pady=(8, 0))
frame_origem = tk.Frame(janela)
frame_origem.pack()
for u in ["cm", "m", "km"]:
    tk.Radiobutton(frame_origem, text=u, variable=origem, value=u).pack(side="left", padx=5)

tk.Label(janela, text="Para:").pack(pady=(8, 0))
frame_destino = tk.Frame(janela)
frame_destino.pack()
for u in ["cm", "m", "km"]:
    tk.Radiobutton(frame_destino, text=u, variable=destino, value=u).pack(side="left", padx=5)

label_resultado = tk.Label(janela, text="", font=("Arial", 11))
label_resultado.pack(pady=(10, 0))

label_erro = tk.Label(janela, text="", fg="red")
label_erro.pack()

def converter():
    label_erro.config(text="")
    label_resultado.config(text="")

    valor_str = entry_valor.get().strip()

    if not valor_str:
        label_erro.config(text="Campo de valor não pode ser vazio.")
        return

    try:
        valor = float(valor_str)
    except ValueError:
        label_erro.config(text="Digite um número válido.")
        return

    if valor <= 0:
        label_erro.config(text="O valor deve ser maior que zero.")
        return

    de = origem.get()
    para = destino.get()

    valor_cm = valor * fatores[de]
    resultado = valor_cm / fatores[para]

    label_resultado.config(text=f"{valor:.2f} {de} = {resultado:.2f} {para}")

def limpar():
    entry_valor.delete(0, tk.END)
    origem.set("cm")
    destino.set("m")
    label_resultado.config(text="")
    label_erro.config(text="")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)
tk.Button(frame_botoes, text="Converter", command=converter).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

janela.mainloop()