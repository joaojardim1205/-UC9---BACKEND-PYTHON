import tkinter as tk

janela = tk.Tk()
janela.title("Calculadora de Gorjeta")
janela.geometry("350x350")

tk.Label(janela, text="Valor da conta (R$):").pack(pady=(15, 0))
entry_conta = tk.Entry(janela, justify="center")
entry_conta.pack()

tk.Label(janela, text="Porcentagem da gorjeta (%):").pack(pady=(10, 0))
entry_pct = tk.Entry(janela, justify="center")
entry_pct.pack()

tk.Label(janela, text="Atalhos:").pack(pady=(10, 0))
frame_atalhos = tk.Frame(janela)
frame_atalhos.pack()

def set_pct(valor):
    entry_pct.delete(0, tk.END)
    entry_pct.insert(0, str(valor))

for p in [10, 15, 18, 20]:
    tk.Button(frame_atalhos, text=f"{p}%", width=5, command=lambda v=p: set_pct(v)).pack(side="left", padx=4)

label_erro = tk.Label(janela, text="", fg="red")
label_erro.pack(pady=(8, 0))

label_gorjeta = tk.Label(janela, text="")
label_gorjeta.pack()

label_total = tk.Label(janela, text="")
label_total.pack()

label_resumo = tk.Label(janela, text="", font=("Arial", 10, "bold"))
label_resumo.pack(pady=(5, 0))

def calcular():
    label_erro.config(text="")
    label_gorjeta.config(text="")
    label_total.config(text="")
    label_resumo.config(text="")

    conta_str = entry_conta.get().strip()
    pct_str = entry_pct.get().strip()

    if not conta_str or not pct_str:
        label_erro.config(text="Preencha todos os campos.")
        return

    try:
        conta = float(conta_str)
        pct = float(pct_str)
    except ValueError:
        label_erro.config(text="Digite números válidos.")
        return

    if conta <= 0 or pct <= 0:
        label_erro.config(text="Os valores devem ser positivos.")
        return

    gorjeta = conta * pct / 100
    total = conta + gorjeta

    label_gorjeta.config(text=f"Gorjeta: R$ {gorjeta:.2f}")
    label_total.config(text=f"Total: R$ {total:.2f}")
    label_resumo.config(text=f"Gorjeta: {pct:.0f}% de R$ {conta:.2f} = R$ {gorjeta:.2f}")

def limpar():
    entry_conta.delete(0, tk.END)
    entry_pct.delete(0, tk.END)
    label_erro.config(text="")
    label_gorjeta.config(text="")
    label_total.config(text="")
    label_resumo.config(text="")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=12)
tk.Button(frame_botoes, text="Calcular", command=calcular).pack(side="left", padx=5)
tk.Button(frame_botoes, text="Limpar", command=limpar).pack(side="left", padx=5)

janela.mainloop()