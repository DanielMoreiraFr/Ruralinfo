import tkinter as tk
from tkinter import ttk
import tkinter
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu

from banco.banco_usuarios import *
from Interface.entidades.infos import MuralInformativo

# Classe que gerencia tanto a tela de Login quanto a de Cadastro
class TelaUsuario(CTk):
    def __init__(self, modo="login"): # O parâmetro 'modo' define o comportamento da tela [ entre login e cadastro ]
        super().__init__()
        self.modo = modo
        self.title(f"{self.modo.capitalize()}")
        self.geometry("700x500")

        # Frame principal que serve como plano de fundo
        self.frame = CTkFrame(self)
        self.frame.pack(fill="both", expand=True)

        # Container que mantém todos os campos agrupados no meio da janela
        self.container = CTkFrame(self.frame, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Título dinâmico (login ou cadastro)
        self.label = CTkLabel(self.container, text=self.modo.capitalize(), font=("Arial", 20))
        self.label.pack(pady=10)

        # campos para ambos os modos
        self.Menu_tipoConta = CTkOptionMenu(self.container, values=["Comum", "Administrador"])
        self.Menu_tipoConta.pack(pady=10)

        # Campo NOME para "cadastro"
        if self.modo == "cadastro":
            self.Entry_nome = CTkEntry(self.container, placeholder_text="Nome completo")
            self.Entry_nome.pack(pady=10)

        self.Entry_email = CTkEntry(self.container, placeholder_text="E-mail '@ufrpe.br'")
        self.Entry_email.pack(pady=10)

        self.Entry_senha = CTkEntry(self.container, placeholder_text="Senha", show="*")
        self.Entry_senha.pack(pady=10)

        # Campo CONFIRMAR SENHA para "cadastro"
        if self.modo == "cadastro":
            self.Entry_confirma_senha = CTkEntry(self.container, placeholder_text="Confirme a senha", show="*")
            self.Entry_confirma_senha.pack(pady=10)

        # cria botão principal com texto e função baseados no modo (login ou cadastro)
        # Escolhe o texto e a função (comando) com base no modo da tela
        texto_botao = "Cadastrar" if self.modo == "cadastro" else "Entrar"
        comando_botao = self.cadastrar_usuario if self.modo == "cadastro" else self.login_usuario # ao descobri qual a ação seleciona o metodo para o botão
        
        self.button_principal = CTkButton(self.container, text=texto_botao, command=comando_botao)
        self.button_principal.pack(pady=20)
        
        # botão para fechar a janela atual
        self.button_voltar = CTkButton(self.container, text="Voltar", command=self.destroy, fg_color="red", hover_color="#8B0000")
        self.button_voltar.pack(pady=10)

    # validação e execução de Login
    def login_usuario(self):
        email = self.Entry_email.get()
        senha = self.Entry_senha.get()
        tipoC = self.Menu_tipoConta.get()

        valid = validação_login(email, senha, tipoC)
        
        if valid[0]:
            dados_usuario = valid[1] 
            
            tkinter.messagebox.showinfo("Sucesso", f"Bem-vindo, {dados_usuario['nome']}!")
            
            id_do_usuario = dados_usuario['id'] 
            tipo_do_usuario = tipoC.lower()

            self.destroy() # Fecha a tela de login
            
            app_mural = MuralInformativo(
                tipo_usuario=tipo_do_usuario, 
                id_usuario=id_do_usuario
            )

            app_mural.mainloop()
        else:
            tkinter.messagebox.showerror("Erro", "Credenciais incorretas!")


    # validação e execução de Cadastro
    def cadastrar_usuario(self):
        nome = self.Entry_nome.get()
        email = self.Entry_email.get()
        senha = self.Entry_senha.get()
        confirma_senha = self.Entry_confirma_senha.get()
        tipoC = self.Menu_tipoConta.get()

        # validações de Segurança e Formato // tratamento de erro
        if email == "":
            tkinter.messagebox.showerror("Erro", "O email não pode ser vazio!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif not email.endswith("@ufrpe.br"):
            tkinter.messagebox.showerror("Erro", "O email deve terminar com '@ufrpe.br'!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif senha != confirma_senha:
            tkinter.messagebox.showerror("Erro", "As senhas não coincidem!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif senha == "":
            tkinter.messagebox.showerror("Erro", "A senha não pode ser vazia!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif len(senha) < 10:
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos 10 caracteres!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif not any(char.isdigit() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos um número!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif not any(char.isalpha() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos uma letra!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos um caractere especial!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif not any(char.isupper() for char in senha):
            tkinter.messagebox.showerror("Erro", "A senha deve conter pelo menos uma letra maiúscula!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
        elif tipoC not in ["Administrador", "Comum"]:
            tkinter.messagebox.showerror("Erro", "Por favor, selecione um tipo de conta válido!")
            self.destroy()
            janela_cadastro = TelaUsuario(modo="cadastro")
            janela_cadastro.mainloop()
            return
         # Verifica se o usuário já existe antes de inserir no banco
        if not usuario_existe(email, tipoC):
            inserir_usuario(nome, email, senha, tipoC)
            tkinter.messagebox.showinfo("Sucesso", "Usuário criado!")
            self.destroy()
        else:
            tkinter.messagebox.showerror("Erro", "Usuário já existe!")
            self.destroy()
            janela_login = TelaUsuario(modo="login")
            janela_login.mainloop()