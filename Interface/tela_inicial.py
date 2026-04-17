import tkinter as tk
from tkinter import ttk
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton

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
        
    def visitante(self):
        print("Botão 'Visitante' pressionado")
    
    def login(self):
        print("Botão 'Login' pressionado")
        
    def cadastrar(self):
        print("Botão 'Cadastrar' pressionado")

if __name__ == "__main__":
    app = TelaInicial()
    app.mainloop()