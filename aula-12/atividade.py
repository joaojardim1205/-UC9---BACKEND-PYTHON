import tkinter as tk
from tkinter import messagebox
import sqlite3

class SistemaCRUD:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema CRUD")
        self.janela.geometry("600x500")
        
        self.cliente_selecionado_id = None
        
        self.criar_banco()
        self.criar_interface()
        self.carregar_lista()
    
    def criar_banco(self):
        conexao = sqlite3.connect("clientes.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT,
                telefone TEXT
            )
        """)
        conexao.commit()
        conexao.close()
    
    def criar_interface(self):
        frame_form = tk.LabelFrame(self.janela, text="Dados do Cliente", padx=10, pady=10)
        frame_form.pack(pady=10, padx=10, fill="x")
        
        tk.Label(frame_form, text="Nome:").grid(row=0, column=0, pady=5)
        self.entry_nome = tk.Entry(frame_form, width=30)
        self.entry_nome.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(frame_form, text="Email:").grid(row=1, column=0, pady=5)
        self.entry_email = tk.Entry(frame_form, width=30)
        self.entry_email.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(frame_form, text="Telefone:").grid(row=2, column=0, pady=5)
        self.entry_telefone = tk.Entry(frame_form, width=30)
        self.entry_telefone.grid(row=2, column=1, pady=5, padx=5)
        
        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)
        
        self.btn_salvar = tk.Button(frame_botoes, text="💾 Salvar", command=self.salvar_cliente,
                                    bg="green", fg="white", width=10)
        self.btn_salvar.pack(side="left", padx=5)
        
        self.btn_atualizar = tk.Button(frame_botoes, text="✏️ Atualizar", command=self.atualizar_cliente,
                                       bg="blue", fg="white", width=10, state="disabled")
        self.btn_atualizar.pack(side="left", padx=5)
        
        self.btn_cancelar = tk.Button(frame_botoes, text="❌ Cancelar", command=self.cancelar_edicao,
                                      bg="gray", fg="white", width=10, state="disabled")
        self.btn_cancelar.pack(side="left", padx=5)
        
        frame_lista = tk.LabelFrame(self.janela, text="Clientes Cadastrados", padx=10, pady=10)
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")
        
        self.listbox_clientes = tk.Listbox(frame_lista, height=10, yscrollcommand=scrollbar.set)
        self.listbox_clientes.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_clientes.yview)
        
        self.listbox_clientes.bind("<<ListboxSelect>>", self.selecionar_cliente)
        
        self.btn_deletar = tk.Button(self.janela, text="🗑 Deletar", command=self.deletar_cliente,
                                     bg="red", fg="white", width=15)
        self.btn_deletar.pack(pady=5)
    
    def salvar_cliente(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO clientes (nome, email, telefone)
                VALUES (?, ?, ?)
            """, (nome, self.entry_email.get(), self.entry_telefone.get()))
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", "Cliente salvo!")
            self.limpar_campos()
            self.carregar_lista()
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao salvar: {erro}")
    
    def carregar_lista(self):
        self.listbox_clientes.delete(0, tk.END)
        
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, email, telefone FROM clientes ORDER BY nome")
            clientes = cursor.fetchall()
            conexao.close()
            
            for cliente in clientes:
                texto = f"[{cliente[0]}] {cliente[1]}"
                if cliente[2]:
                    texto += f" - {cliente[2]}"
                self.listbox_clientes.insert(tk.END, texto)
                self.listbox_clientes.itemconfig("end", {"id": cliente[0]})
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao carregar: {erro}")
    
    def selecionar_cliente(self, event):
        selecao = self.listbox_clientes.curselection()
        if not selecao:
            return
        
        texto = self.listbox_clientes.get(selecao[0])
        
        try:
            id_str = texto.split("]")[0].replace("[", "")
            self.cliente_selecionado_id = int(id_str)
            
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome, email, telefone FROM clientes WHERE id = ?",
                           (self.cliente_selecionado_id,))
            cliente = cursor.fetchone()
            conexao.close()
            
            if cliente:
                self.entry_nome.delete(0, tk.END)
                self.entry_nome.insert(0, cliente[0])
                
                self.entry_email.delete(0, tk.END)
                self.entry_email.insert(0, cliente[1] if cliente[1] else "")
                
                self.entry_telefone.delete(0, tk.END)
                self.entry_telefone.insert(0, cliente[2] if cliente[2] else "")
                
                self.btn_salvar.config(state="disabled")
                self.btn_atualizar.config(state="normal")
                self.btn_cancelar.config(state="normal")
        
        except (ValueError, IndexError, sqlite3.Error):
            messagebox.showerror("Erro", "Erro ao selecionar cliente")
    
    def atualizar_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado!")
            return
        
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Nome é obrigatório!")
            return
        
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nome = ?, email = ?, telefone = ?
                WHERE id = ?
            """, (nome, self.entry_email.get(), self.entry_telefone.get(),
                  self.cliente_selecionado_id))
            conexao.commit()
            conexao.close()
            
            messagebox.showinfo("Sucesso", "Cliente atualizado!")
            self.cancelar_edicao()
            self.carregar_lista()
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao atualizar: {erro}")
    
    def deletar_cliente(self):
        if not self.cliente_selecionado_id:
            selecao = self.listbox_clientes.curselection()
            if not selecao:
                messagebox.showwarning("Aviso", "Selecione um cliente para deletar!")
                return
            
            texto = self.listbox_clientes.get(selecao[0])
            id_str = texto.split("]")[0].replace("[", "")
            self.cliente_selecionado_id = int(id_str)
        
        try:
            conexao = sqlite3.connect("clientes.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM clientes WHERE id = ?",
                           (self.cliente_selecionado_id,))
            cliente = cursor.fetchone()
            conexao.close()
            
            if cliente:
                if messagebox.askyesno("Confirmar Exclusão",
                                       f"Tem certeza que deseja excluir\n{cliente[0]}?"):
                    conexao = sqlite3.connect("clientes.db")
                    cursor = conexao.cursor()
                    cursor.execute("DELETE FROM clientes WHERE id = ?",
                                   (self.cliente_selecionado_id,))
                    conexao.commit()
                    conexao.close()
                    
                    messagebox.showinfo("Sucesso", "Cliente excluído!")
                    self.cancelar_edicao()
                    self.carregar_lista()
            else:
                messagebox.showwarning("Aviso", "Cliente não encontrado!")
        
        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao deletar: {erro}")
    
    def cancelar_edicao(self):
        self.limpar_campos()
        self.cliente_selecionado_id = None
        self.btn_salvar.config(state="normal")
        self.btn_atualizar.config(state="disabled")
        self.btn_cancelar.config(state="disabled")
        self.listbox_clientes.selection_clear(0, tk.END)
    
    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)

janela = tk.Tk()
app = SistemaCRUD(janela)
janela.mainloop()