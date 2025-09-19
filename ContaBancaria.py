import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "contas.db"


# ------------------ Banco de Dados ------------------
class Database:
    def __init__(self, db_file=DB_FILE):
        self.conn = sqlite3.connect(db_file)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            numero_conta TEXT NOT NULL UNIQUE,
            saldo REAL DEFAULT 0
        )
        """)
        self.conn.commit()

    def criar_conta(self, nome, numero_conta, saldo=0):
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO contas (nome, numero_conta, saldo) VALUES (?, ?, ?)",
                        (nome, numero_conta, saldo))
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Número de conta já existe.")
            return None

    def atualizar_saldo(self, numero_conta, novo_saldo):
        self.conn.execute("UPDATE contas SET saldo=? WHERE numero_conta=?",
                          (novo_saldo, numero_conta))
        self.conn.commit()

    def buscar_conta(self, numero_conta):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contas WHERE numero_conta=?", (numero_conta,))
        return cur.fetchone()

    def listar_contas(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM contas ORDER BY id DESC")
        return cur.fetchall()


# ------------------ Aplicativo Tkinter ------------------
class App(tk.Tk):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.title("Banco Tkinter + SQLite")
        self.geometry("600x400")
        self.resizable(False, False)

        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        frm_top = ttk.Frame(self, padding=10)
        frm_top.pack(fill=tk.X)

        ttk.Label(frm_top, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_nome = ttk.Entry(frm_top, width=20)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frm_top, text="Número Conta:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_numero = ttk.Entry(frm_top, width=15)
        self.entry_numero.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frm_top, text="Valor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_valor = ttk.Entry(frm_top, width=20)
        self.entry_valor.grid(row=1, column=1, padx=5, pady=5)

        # Botões
        frm_buttons = ttk.Frame(frm_top)
        frm_buttons.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frm_buttons, text="Criar Conta", command=self.criar_conta).pack(side=tk.LEFT, padx=3)
        ttk.Button(frm_buttons, text="Depositar", command=self.depositar).pack(side=tk.LEFT, padx=3)
        ttk.Button(frm_buttons, text="Sacar", command=self.sacar).pack(side=tk.LEFT, padx=3)
        ttk.Button(frm_buttons, text="Exibir Saldo", command=self.exibir_saldo).pack(side=tk.LEFT, padx=3)

        # Treeview para listar contas
        columns = ("id", "nome", "numero", "saldo")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("numero", text="Conta")
        self.tree.heading("saldo", text="Saldo")

        self.tree.column("id", width=40, anchor=tk.CENTER)
        self.tree.column("nome", width=180)
        self.tree.column("numero", width=120, anchor=tk.CENTER)
        self.tree.column("saldo", width=100, anchor=tk.E)

        self.tree.pack(padx=10, pady=10, fill=tk.BOTH)

    # ------------------ Funções ------------------
    def criar_conta(self):
        nome = self.entry_nome.get().strip()
        numero = self.entry_numero.get().strip()
        if not nome or not numero:
            messagebox.showwarning("Aviso", "Preencha nome e número da conta.")
            return
        rid = self.db.criar_conta(nome, numero, 0)
        if rid:
            messagebox.showinfo("Sucesso", f"Conta criada com ID {rid}")
            self.refresh_tree()

    def depositar(self):
        numero = self.entry_numero.get().strip()
        try:
            valor = float(self.entry_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")
            return
        conta = self.db.buscar_conta(numero)
        if conta:
            novo_saldo = conta["saldo"] + valor
            self.db.atualizar_saldo(numero, novo_saldo)
            messagebox.showinfo("Sucesso", f"Depósito de R${valor:.2f} realizado.")
            self.refresh_tree()
        else:
            messagebox.showerror("Erro", "Conta não encontrada.")

    def sacar(self):
        numero = self.entry_numero.get().strip()
        try:
            valor = float(self.entry_valor.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido.")
            return
        conta = self.db.buscar_conta(numero)
        if conta:
            if valor <= 0 or valor > conta["saldo"]:
                messagebox.showwarning("Aviso", "Saldo insuficiente ou valor inválido.")
                return
            novo_saldo = conta["saldo"] - valor
            self.db.atualizar_saldo(numero, novo_saldo)
            messagebox.showinfo("Sucesso", f"Saque de R${valor:.2f} realizado.")
            self.refresh_tree()
        else:
            messagebox.showerror("Erro", "Conta não encontrada.")

    def exibir_saldo(self):
        numero = self.entry_numero.get().strip()
        conta = self.db.buscar_conta(numero)
        if conta:
            messagebox.showinfo("Saldo",
                                f"Nome: {conta['nome']}\nConta: {conta['numero_conta']}\nSaldo: R${conta['saldo']:.2f}")
        else:
            messagebox.showerror("Erro", "Conta não encontrada.")

    def refresh_tree(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        for conta in self.db.listar_contas():
            self.tree.insert("", tk.END, values=(conta["id"], conta["nome"],
                                                 conta["numero_conta"], f"R${conta['saldo']:.2f}"))


if __name__ == "__main__":
    db = Database()
    app = App(db)
    app.mainloop()
