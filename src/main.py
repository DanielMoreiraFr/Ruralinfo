import tkinter as tk
from tkinter import ttk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton
import tkinter.messagebox
from Interface.entidades import usuarios, infos

# cria frame para a tela inicial, onde o usuário pode escolher entre visitante, login ou cadastro
class TelaInicial(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ruralinfo - Tela Inicial")
        self.geometry("800x600")

        # Frame principal que ocupa toda a janela
        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Frame 'container' invisível para centralizar os itens agrupados
        # O place com relx e rely 0.5 coloca este frame exatamente no centro do self.frame
        self.container = CTkFrame(self.frame, fg_color="transparent")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Todos os widgets agora são empacotados (pack) dentro do self.container
        self.label = CTkLabel(self.container, text="Bem Vinda(o) ao Ruralinfo!")
        self.label.pack(pady=10)

        # Botão para acesso como visitante
        self.button_visitante = CTkButton(self.container, text="Visitante", command=self.visitante)
        self.button_visitante.pack(pady=10)
        
        # Botão para abrir a tela de login
        self.button_login = CTkButton(self.container, text="Login", command=self.login)
        self.button_login.pack(pady=10)
        
        # Botão para abrir a tela de cadastro
        self.button_cadastrar = CTkButton(self.container, text="Cadastrar", command=self.cadastrar)
        self.button_cadastrar.pack(pady=10)

        # Botão de sair/voltar com cor personalizada
        self.button_voltar = CTkButton(self.container, text="Sair", command=self.destroy, fg_color="red", hover_color="#8B0000")
        self.button_voltar.pack(pady=10)

# Métodos que definem o comportamento de cada botão
    def visitante(self):
        print('Botão "Visitante" pressionado')
        # Criamos a instância da tela de usuário configurada para o modo visitante
        app_mural = infos.MuralInformativo(tipo_usuario="visitante")
        app_mural.mainloop()

    def login(self):
        print('Botão "Login" pressionado')
        # Criamos a instância da tela de usuário configurada para o modo login
        janela_login = usuarios.TelaUsuario(modo="login")
        janela_login.mainloop()

    def cadastrar(self):
        print('Botão "Cadastrar" pressionado')
        # Criamos a instância da tela de usuário configurada para o modo cadastro
        janela_cad = usuarios.TelaUsuario(modo="cadastro")
        janela_cad.mainloop()

    def voltar(self):
        # Fecha a janela atual
        self.destroy()

# Ponto de entrada do script
if __name__ == "__main__":
    app = TelaInicial()
    app.mainloop()