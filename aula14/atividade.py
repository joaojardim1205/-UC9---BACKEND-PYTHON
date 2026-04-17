import tkinter as tk
from tkinter import messagebox
import sqlite3

class SistemaCRUD:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema CRUD - Clínica Veterinária")
        self.janela.geometry("700x650")

        self.cliente_selecionado_id = None

        self.criar_banco()
        self.criar_interface()
        self.carregar_lista()

    def criar_banco(self):
        conexao = sqlite3.connect("clinica_vet_crud.db")
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_pet TEXT NOT NULL,
                especie TEXT,
                peso REAL,
                nome_responsavel TEXT,
                email TEXT,
                telefone TEXT,
                endereco TEXT
            )
        """)
        conexao.commit()
        conexao.close()

    def criar_interface(self):
        frame_form = tk.LabelFrame(self.janela, text="Dados do Pet e Responsável", padx=10, pady=10)
        frame_form.pack(pady=10, padx=10, fill="x")

        tk.Label(frame_form, text="Nome do Pet:").grid(row=0, column=0, pady=5, sticky="e")
        self.entry_nome_pet = tk.Entry(frame_form, width=40)
        self.entry_nome_pet.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Espécie:").grid(row=1, column=0, pady=5, sticky="e")
        self.entry_especie = tk.Entry(frame_form, width=40)
        self.entry_especie.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Peso (kg):").grid(row=2, column=0, pady=5, sticky="e")
        self.entry_peso = tk.Entry(frame_form, width=40)
        self.entry_peso.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Nome do Responsável:").grid(row=3, column=0, pady=5, sticky="e")
        self.entry_nome_responsavel = tk.Entry(frame_form, width=40)
        self.entry_nome_responsavel.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Email:").grid(row=4, column=0, pady=5, sticky="e")
        self.entry_email = tk.Entry(frame_form, width=40)
        self.entry_email.grid(row=4, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Telefone:").grid(row=5, column=0, pady=5, sticky="e")
        self.entry_telefone = tk.Entry(frame_form, width=40)
        self.entry_telefone.grid(row=5, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Endereço:").grid(row=6, column=0, pady=5, sticky="e")
        self.entry_endereco = tk.Entry(frame_form, width=40)
        self.entry_endereco.grid(row=6, column=1, pady=5, padx=5)

        frame_botoes = tk.Frame(self.janela)
        frame_botoes.pack(pady=10)

        self.btn_salvar = tk.Button(frame_botoes, text="💾 Salvar", command=self.salvar_cliente,
                                    bg="green", fg="white", width=10)
        self.btn_salvar.pack(side="left", padx=5)

        self.btn_editar = tk.Button(frame_botoes, text="✏️ Editar", command=self.editar_cliente,
                                    bg="orange", fg="white", width=10)
        self.btn_editar.pack(side="left", padx=5)

        self.btn_atualizar = tk.Button(frame_botoes, text="🔄 Atualizar", command=self.atualizar_cliente,
                                       bg="blue", fg="white", width=10, state="disabled")
        self.btn_atualizar.pack(side="left", padx=5)

        self.btn_excluir = tk.Button(frame_botoes, text="🗑 Excluir", command=self.excluir_cliente,
                                     bg="red", fg="white", width=10)
        self.btn_excluir.pack(side="left", padx=5)

        self.btn_cancelar = tk.Button(frame_botoes, text="❌ Cancelar", command=self.cancelar_edicao,
                                      bg="gray", fg="white", width=10)
        self.btn_cancelar.pack(side="left", padx=5)

        frame_lista = tk.LabelFrame(self.janela, text="Pets Cadastrados", padx=10, pady=10)
        frame_lista.pack(pady=10, padx=10, fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")

        self.listbox_clientes = tk.Listbox(frame_lista, height=8, yscrollcommand=scrollbar.set)
        self.listbox_clientes.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox_clientes.yview)

        self.lbl_status = tk.Label(self.janela, text="Pronto.", bd=1, relief="sunken",
                                   anchor="w", padx=8, bg="#f0f0f0", fg="#333333")
        self.lbl_status.pack(fill="x", side="bottom", ipady=3)

    def set_status(self, msg):
        self.lbl_status.config(text=msg)

    def salvar_cliente(self):
        nome_pet = self.entry_nome_pet.get().strip()
        if not nome_pet:
            messagebox.showwarning("Aviso", "Nome do Pet é obrigatório!")
            return

        peso_str = self.entry_peso.get().strip()
        peso = None
        if peso_str:
            try:
                peso = float(peso_str.replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Peso deve ser um número válido (ex: 4.5)")
                return

        try:
            conexao = sqlite3.connect("clinica_vet_crud.db")
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO clientes (nome_pet, especie, peso, nome_responsavel, email, telefone, endereco)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome_pet, self.entry_especie.get().strip(), peso,
                  self.entry_nome_responsavel.get().strip(),
                  self.entry_email.get().strip(),
                  self.entry_telefone.get().strip(),
                  self.entry_endereco.get().strip()))
            conexao.commit()
            conexao.close()

            self.limpar_campos()
            self.carregar_lista()
            self.set_status(f"Pet '{nome_pet}' salvo com sucesso.")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao salvar: {erro}")

    def carregar_lista(self):
        self.listbox_clientes.delete(0, tk.END)

        try:
            conexao = sqlite3.connect("clinica_vet_crud.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome_pet, nome_responsavel FROM clientes ORDER BY nome_pet")
            clientes = cursor.fetchall()
            conexao.close()

            for cliente in clientes:
                texto = f"[{cliente[0]}] {cliente[1]}"
                if cliente[2]:
                    texto += f" - {cliente[2]}"
                self.listbox_clientes.insert(tk.END, texto)

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao carregar: {erro}")

    def editar_cliente(self):
        selecao = self.listbox_clientes.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um pet na lista para editar!")
            return

        texto = self.listbox_clientes.get(selecao[0])

        try:
            id_str = texto.split("]")[0].replace("[", "")
            self.cliente_selecionado_id = int(id_str)

            conexao = sqlite3.connect("clinica_vet_crud.db")
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT nome_pet, especie, peso, nome_responsavel, email, telefone, endereco
                FROM clientes WHERE id = ?
            """, (self.cliente_selecionado_id,))
            cliente = cursor.fetchone()
            conexao.close()

            if cliente:
                self.limpar_campos()
                self.entry_nome_pet.insert(0, cliente[0])
                self.entry_especie.insert(0, cliente[1] if cliente[1] else "")
                self.entry_peso.insert(0, str(cliente[2]) if cliente[2] is not None else "")
                self.entry_nome_responsavel.insert(0, cliente[3] if cliente[3] else "")
                self.entry_email.insert(0, cliente[4] if cliente[4] else "")
                self.entry_telefone.insert(0, cliente[5] if cliente[5] else "")
                self.entry_endereco.insert(0, cliente[6] if cliente[6] else "")

                self.btn_salvar.config(state="disabled")
                self.btn_atualizar.config(state="normal")
                self.set_status(f"Editando pet ID {self.cliente_selecionado_id}: {cliente[0]}.")

        except (ValueError, IndexError, sqlite3.Error):
            messagebox.showerror("Erro", "Erro ao carregar dados do pet.")

    def atualizar_cliente(self):
        if not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Nenhum pet em edição!")
            return

        nome_pet = self.entry_nome_pet.get().strip()
        if not nome_pet:
            messagebox.showwarning("Aviso", "Nome do Pet é obrigatório!")
            return

        peso_str = self.entry_peso.get().strip()
        peso = None
        if peso_str:
            try:
                peso = float(peso_str.replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Peso deve ser um número válido (ex: 4.5)")
                return

        try:
            conexao = sqlite3.connect("clinica_vet_crud.db")
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE clientes
                SET nome_pet = ?, especie = ?, peso = ?, nome_responsavel = ?,
                    email = ?, telefone = ?, endereco = ?
                WHERE id = ?
            """, (nome_pet, self.entry_especie.get().strip(), peso,
                  self.entry_nome_responsavel.get().strip(),
                  self.entry_email.get().strip(),
                  self.entry_telefone.get().strip(),
                  self.entry_endereco.get().strip(),
                  self.cliente_selecionado_id))
            conexao.commit()
            conexao.close()

            self.cancelar_edicao()
            self.carregar_lista()
            self.set_status(f"Pet '{nome_pet}' atualizado com sucesso.")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao atualizar: {erro}")

    def excluir_cliente(self):
        selecao = self.listbox_clientes.curselection()
        if not selecao and not self.cliente_selecionado_id:
            messagebox.showwarning("Aviso", "Selecione um pet para excluir!")
            return

        if not self.cliente_selecionado_id:
            texto = self.listbox_clientes.get(selecao[0])
            id_str = texto.split("]")[0].replace("[", "")
            self.cliente_selecionado_id = int(id_str)

        try:
            conexao = sqlite3.connect("clinica_vet_crud.db")
            cursor = conexao.cursor()
            cursor.execute("SELECT nome_pet, nome_responsavel FROM clientes WHERE id = ?",
                           (self.cliente_selecionado_id,))
            cliente = cursor.fetchone()
            conexao.close()

            if not cliente:
                messagebox.showwarning("Aviso", "Pet não encontrado!")
                return

            if messagebox.askyesno("Confirmar Exclusão",
                                   f"Tem certeza que deseja excluir:\n\nPet: {cliente[0]}\nResponsável: {cliente[1]}?"):
                conexao = sqlite3.connect("clinica_vet_crud.db")
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = ?",
                               (self.cliente_selecionado_id,))
                conexao.commit()
                conexao.close()

                self.cancelar_edicao()
                self.carregar_lista()
                self.set_status(f"Pet '{cliente[0]}' excluído com sucesso.")

        except sqlite3.Error as erro:
            messagebox.showerror("Erro", f"Erro ao excluir: {erro}")

    def cancelar_edicao(self):
        self.limpar_campos()
        self.cliente_selecionado_id = None
        self.btn_salvar.config(state="normal")
        self.btn_atualizar.config(state="disabled")
        self.listbox_clientes.selection_clear(0, tk.END)
        self.set_status("Operação cancelada. Formulário limpo.")

    def limpar_campos(self):
        for entry in (self.entry_nome_pet, self.entry_especie, self.entry_peso,
                      self.entry_nome_responsavel, self.entry_email,
                      self.entry_telefone, self.entry_endereco):
            entry.delete(0, tk.END)


janela = tk.Tk()
app = SistemaCRUD(janela)
janela.mainloop()