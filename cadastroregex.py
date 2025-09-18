import tkinter as tk
from tkinter import messagebox
import re
import sqlite3
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            cpf TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def inserir_usuario(nome, email, cpf, senha):
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios (nome, email, cpf, senha)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, cpf, senha))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError as e:
        return False

def validar_nome(nome):
    return re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome) is not None

def validar_email(email):
    return re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email) is not None

def validar_cpf(cpf):
    return re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) is not None

def validar_senha(senha):
    return re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", senha) is not None

def cadastrar():
    nome = entry_nome.get()
    email = entry_email.get()
    cpf = entry_cpf.get()
    senha = entry_senha.get()

    if not validar_nome(nome):
        messagebox.showerror("Erro", "Nome inválido. Use apenas letras e espaços.")
        return
    if not validar_email(email):
        messagebox.showerror("Erro", "Email inválido.")
        return
    if not validar_cpf(cpf):
        messagebox.showerror("Erro", "CPF inválido. Use o formato 000.000.000-00.")
        return
    if not validar_senha(senha):
        messagebox.showerror("Erro", "Senha fraca. Use no mínimo 8 caracteres, com letras e números.")
        return

    sucesso = inserir_usuario(nome, email, cpf, senha)
    if sucesso:
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Usuário já existe ou erro no cadastro.")

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_senha.delete(0, tk.END)

criar_banco()

janela = tk.Tk()
janela.title("Cadastro de Usuário")
janela.geometry("400x300")

tk.Label(janela, text="Nome completo").pack()
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack()

tk.Label(janela, text="Email").pack()
entry_email = tk.Entry(janela, width=40)
entry_email.pack()

tk.Label(janela, text="CPF (000.000.000-00)").pack()
entry_cpf = tk.Entry(janela, width=40)
entry_cpf.pack()

tk.Label(janela, text="Senha").pack()
entry_senha = tk.Entry(janela, width=40, show="*")
entry_senha.pack()

tk.Button(janela, text="Cadastrar", command=cadastrar, bg="#4CAF50", fg="white").pack(pady=10)

janela.mainloop()
