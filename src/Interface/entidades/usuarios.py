import tkinter as tk
from tkinter import ttk
import tkinter
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu
from banco.banco_usuarios import *

# cria frame para a tela de cadastro, onde o usuário pode escolher o tipo de conta, inserir email e senha
class CadastroUsuario(CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro")
        self.geometry("300x400")

        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = CTkLabel(self.frame, text="Cadastro")
        self.label.pack(pady=10)

        self.Menu_tipoConta = CTkOptionMenu(self.frame, values=["Comum", "Administrador"])
        self.Menu_tipoConta.pack(pady=10)
        
        self.Entry_nome = CTkEntry(self.frame, placeholder_text="insira seu nome completo")
        self.Entry_nome.pack(pady=10)
        
        self.Entry_email = CTkEntry(self.frame, placeholder_text="insira seu e-mail '@ufrpe.br'")
        self.Entry_email.pack(pady=10)
        
        self.Entry_senha = CTkEntry(self.frame, placeholder_text="crie uma senha", show="*")
        self.Entry_senha.pack(pady=10)
        
        self.Entry_confirma_senha = CTkEntry(self.frame, placeholder_text="confirme a senha", show="*")
        self.Entry_confirma_senha.pack(pady=10)
        
        self.button_cadastrar = CTkButton(self.frame, text="Cadastrar", command=self.cadastrar)
        self.button_cadastrar.pack(pady=10)
        
        self.button_voltar = CTkButton(self.frame, text="Voltar", command=self.voltar)
        self.button_voltar.pack(pady=10)
    
    def cadastrar(self):
        email = self.Entry_email.get()
        senha = self.Entry_senha.get()
        confirma_senha = self.Entry_confirma_senha.get()
        nome = self.Entry_nome.get()
        tipoC = self.Menu_tipoConta.get()
        
#tratamentos de erro
        if not email.endswith("@ufrpe.br"):
            tkinter.messagebox.showerror("Erro", "O email deve terminar com '@ufrpe.br'!")
            return
        
        if email == "":
            tkinter.messagebox.showerror("Erro", "O email não pode ser vazio!")
            return
        
        
        if senha != confirma_senha:
            tkinter.messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        if senha == "":
            tkinter.messagebox.showerror("Erro", "A senha não pode ser vazia!")
            return
        
        if len(senha) < 10:
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos 10 caracteres!")
            return
        
        if not any(char.isdigit() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos um número!")
            return
        
        if not any(char.isalpha() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos uma letra!")
            return
        
        if not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos um caractere especial!")
            return
        
        if not any(char.isupper() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos uma letra maiúscula!")
            return
        
        if tipoC not in ["Administrador", "Comum"]:
            tkinter.messagebox.showerror("Erro", "Por favor, selecione um tipo de conta válido!")
            return
        
        if usuario_existe(email, tipoC):
            tkinter.messagebox.showerror("Erro", "Este email já está cadastrado para este tipo de conta!")
            return
        else:
            inserir_usuario(nome, email, senha, tipoC)
            tkinter.messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            
        self.destroy()
            
    def voltar(self):
        self.destroy()


class login_usuario(CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x500")

        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = CTkLabel(self.frame, text="Login")
        self.label.pack(pady=10)

        self.Menu_tipoConta = CTkOptionMenu(self.frame, values=["Comum", "Administrador"])
        self.Menu_tipoConta.pack(pady=10)
        
        self.Entry_email = CTkEntry(self.frame, placeholder_text="Insira seu e-mail")
        self.Entry_email.pack(pady=10)
        
        self.Entry_senha = CTkEntry(self.frame, placeholder_text="Insira sua senha", show="*")
        self.Entry_senha.pack(pady=10)
        
        self.button_login = CTkButton(self.frame, text="Login", command=self.login)
        self.button_login.pack(pady=10)
        
        self.button_voltar = CTkButton(self.frame, text="Voltar", command=self.voltar)
        self.button_voltar.pack(pady=10)
    

    def login(self):
        email = self.Entry_email.get()
        senha = self.Entry_senha.get()
        tipoC = self.Menu_tipoConta.get()

        valid = validação_login(email, senha, tipoC)

        if valid[0]:
            tkinter.messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.destroy()
        else:
            tkinter.messagebox.showinfo('Erro', "Email, senha ou tipo de conta incorreto!")
            return


    def voltar(self):
        self.destroy()