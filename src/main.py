import tkinter as tk
from tkinter import ttk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton
import tkinter.messagebox
from Interface import cadastro_usuario

# desculpa, esqueci dos comentários

# cria frame para a tela inicial, onde o usuário pode escolher entre visitante, login ou cadastro
class TelaInicial(CTk):
    def __init__(self):
        super().__init__()
        self.title("Ruralinfo - Tela Inicial")
        self.geometry("300x400")

        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = CTkLabel(self.frame, text="Bem Vinda(o) ao Ruralinfo!")
        self.label.pack(pady=10)

        self.button = CTkButton(self.frame, text="Visitante", command=self.visitante)
        self.button.pack(pady=10)
        
        self.button = CTkButton(self.frame, text="Login", command=self.login)
        self.button.pack(pady=10)
        
        self.button = CTkButton(self.frame, text="Cadastrar", command=self.cadastrar)
        self.button.pack(pady=10)
 
# cria botões para cada opção, que por enquanto só imprimem uma mensagem no console
# mas futuramente podem ser conectados a outras telas ou funcionalidades do programa       
    def visitante(self):
        tkinter.messagebox.showinfo("Visitante", "Botão 'Visitante' pressionado")
    
    def login(self):
        tkinter.messagebox.showinfo("Login", "Botão 'Login' pressionado")
        
    def cadastrar(self):
        print("Cadastrar", "Botão 'Cadastrar' pressionado")
        cadastro = cadastro_usuario.CadastroUsuario()
        cadastro.mainloop()

if __name__ == "__main__":
    app = TelaInicial()
    app.mainloop()