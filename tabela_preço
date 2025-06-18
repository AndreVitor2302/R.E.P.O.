import tkinter as tk
from tkinter import messagebox

class Mercado:
    def __init__(self):
        self.tabela_precos = {}
        self.janela = tk.Tk()
        self.janela.title("Gerenciamento de Tabela de Preços")

        # Acesso restrito ao administrador
        self.senha_administrador = "admin123"
        self.acesso_liberado = False

        # Frame de login
        self.frame_login = tk.Frame(self.janela)
        self.frame_login.pack()
        self.label_senha = tk.Label(self.frame_login, text="Senha de Administrador:")
        self.label_senha.pack(side=tk.LEFT)
        self.entry_senha = tk.Entry(self.frame_login, show="*")
        self.entry_senha.pack(side=tk.LEFT)
        self.botao_login = tk.Button(self.frame_login, text="Login", command=self.verificar_senha)
        self.botao_login.pack(side=tk.LEFT)

        # Frame de menu principal (aparece após login)
        self.frame_menu = tk.Frame(self.janela)
        self.frame_menu.pack_forget()
        self.botao_inserir = tk.Button(self.frame_menu, text="Inserir Preço", command=self.inserir_preco)
        self.botao_inserir.pack(side=tk.LEFT)
        self.botao_remover = tk.Button(self.frame_menu, text="Remover Preço", command=self.remover_preco)
        self.botao_remover.pack(side=tk.LEFT)
        self.botao_atualizar = tk.Button(self.frame_menu, text="Atualizar Preço", command=self.atualizar_preco)
        self.botao_atualizar.pack(side=tk.LEFT)
        self.botao_exibir = tk.Button(self.frame_menu, text="Exibir Tabela de Preços", command=self.exibir_tabela)
        self.botao_exibir.pack(side=tk.LEFT)

        # Área de texto para exibição da tabela
        self.text_area = tk.Text(self.janela, height=10, width=50)
        self.text_area.pack_forget()

    def verificar_senha(self):
        senha = self.entry_senha.get()
        if senha == self.senha_administrador:
            self.acesso_liberado = True
            self.frame_login.pack_forget()
            self.frame_menu.pack()
        else:
            messagebox.showerror("Erro", "Senha incorreta. Acesso negado.")

    def inserir_preco(self):
        self.frame_inserir = tk.Toplevel(self.janela)
        self.frame_inserir.title("Inserir Preço")
        tk.Label(self.frame_inserir, text="Nome do Produto:").pack()
        self.entry_produto = tk.Entry(self.frame_inserir)
        self.entry_produto.pack()
        tk.Label(self.frame_inserir, text="Preço do Produto:").pack()
        self.entry_preco = tk.Entry(self.frame_inserir)
        self.entry_preco.pack()
        tk.Button(self.frame_inserir, text="Salvar", command=self.salvar_preco).pack()

    def salvar_preco(self):
        produto = self.entry_produto.get()
        try:
            preco = float(self.entry_preco.get())
            self.tabela_precos[produto] = preco
            messagebox.showinfo("Sucesso", f"Produto '{produto}' inserido com sucesso!")
            self.frame_inserir.destroy()
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o preço.")

    def remover_preco(self):
        self.frame_remover = tk.Toplevel(self.janela)
        self.frame_remover.title("Remover Preço")
        tk.Label(self.frame_remover, text="Nome do Produto:").pack()
        self.entry_produto_remover = tk.Entry(self.frame_remover)
        self.entry_produto_remover.pack()
        tk.Button(self.frame_remover, text="Remover", command=self.remover_produto).pack()

    def remover_produto(self):
        produto = self.entry_produto_remover.get()
        if produto in self.tabela_precos:
            del self.tabela_precos[produto]
            messagebox.showinfo("Sucesso", f"Produto '{produto}' removido com sucesso!")
        else:
            messagebox.showerror("Erro", f"Produto '{produto}' não encontrado na tabela de preços.")
        self.frame_remover.destroy()

    def atualizar_preco(self):
        self.frame_atualizar = tk.Toplevel(self.janela)
        self.frame_atualizar.title("Atualizar Preço")
        tk.Label(self.frame_atualizar, text="Nome do Produto:").pack()
        self.entry_produto_atualizar = tk.Entry(self.frame_atualizar)
        self.entry_produto_atualizar.pack()
        tk.Label(self.frame_atualizar, text="Novo Preço:").pack()
        self.entry_novo_preco = tk.Entry(self.frame_atualizar)
        self.entry_novo_preco.pack()
        tk.Button(self.frame_atualizar, text="Atualizar", command=self.salvar_atualizacao).pack()

    def salvar_atualizacao(self):
        produto = self.entry_produto_atualizar.get()
        if produto in self.tabela_precos:
            try:
                novo_preco = float(self.entry_novo_preco.get())
                self.tabela_precos[produto] = novo_preco
                messagebox.showinfo("Sucesso", f"Preço do produto '{produto}' atualizado para R$ {novo_preco:.2f}!")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o novo preço.")
        else:
            messagebox.showerror("Erro", f"Produto '{produto}' não encontrado na tabela.")
        self.frame_atualizar.destroy()

    def exibir_tabela(self):
        self.text_area.pack()
        self.text_area.delete(1.0, tk.END)
        if not self.tabela_precos:
            self.text_area.insert(tk.END, "Tabela de preços está vazia.\n")
        else:
            self.text_area.insert(tk.END, "Produto\t\tPreço (R$)\n")
            self.text_area.insert(tk.END, "-" * 30 + "\n")
            for produto, preco in self.tabela_precos.items():
                self.text_area.insert(tk.END, f"{produto}\t\tR$ {preco:.2f}\n")

# Iniciar a aplicação
if __name__ == "__main__":
    app = Mercado()
    app.janela.mainloop()
