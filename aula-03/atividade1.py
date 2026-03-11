import tkinter as tk

janela = tk.Tk()
janela.title("Minha Primeira Aplicação Desktop")
janela.geometry("400x300")
janela.configure(bg="lightblue")
janela.resizable(False, False)

janela.update_idletasks()
w = janela.winfo_width()
h = janela.winfo_height()
x = (janela.winfo_screenwidth() // 2) - (w // 2)
y = (janela.winfo_screenheight() // 2) - (h // 2)
janela.geometry(f"{w}x{h}+{x}+{y}")

label = tk.Label(janela, text="Bem-vindo ao Python Desktop!", font=("Arial", 16, "bold"), bg="lightblue", fg="black")
label.pack(expand=True)

janela.mainloop()