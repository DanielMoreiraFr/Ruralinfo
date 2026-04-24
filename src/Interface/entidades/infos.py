import tkinter as tk
from tkinter import ttk
import tkinter
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu
from banco.banco_usuarios import *
from banco.banco_infos import postagem
from banco.banco_usuarios import gerenciar_db
from customtkinter import CTk, CTkFrame, CTkLabel, CTkButton, CTkScrollableFrame

class MuralInformativo(CTk):
    def __init__(self, tipo_usuario="comum"): # Pode ser 'administrador', 'comum' ou 'visitante'
        super().__init__()
        self.tipo_usuario = tipo_usuario
        self.title(f"Ruralinfo - Mural ({self.tipo_usuario.capitalize()})")
        self.geometry("800x600")

        # --- Layout Principal ---
        self.sidebar = CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.conteudo = CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # --- Elementos Fixos (Todos veem) ---
        self.label_titulo = CTkLabel(self.conteudo, text="Mural de Avisos", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

        self.mural_scrolling = CTkScrollableFrame(self.conteudo, label_text="Avisos Recentes")
        self.mural_scrolling.pack(fill="both", expand=True, pady=10)

        # Botão de Menu (Todos veem)
        self.btn_menu = CTkButton(self.sidebar, text="Acessar Menu", command=self.abrir_menu)
        self.btn_menu.pack(pady=20, padx=10)

        # --- Lógica de Permissões (Elementos Condicionais) ---
        self.montar_ferramentas_especificas()
        self.carregar_avisos_no_mural()

    def montar_ferramentas_especificas(self):
        """Injeta botões e campos baseados no nível de acesso"""
        
        if self.tipo_usuario == "administrador":
            self.frame_adm = CTkFrame(self.sidebar, fg_color="transparent")
            self.frame_adm.pack(pady=10, fill="x")

            # Importante: O ADM precisa de um lugar para escrever antes de clicar no botão!
            self.entry_novo_aviso = CTkEntry(self.frame_adm, placeholder_text="Escreva o aviso aqui...")
            self.entry_novo_aviso.pack(pady=5, padx=10)

            # Agora o botão aponta para a função publicar_novo_aviso
            self.btn_add = CTkButton(self.frame_adm, text="+ Adicionar Aviso", 
                                     fg_color="green", hover_color="#1e7b4d",
                                     command=self.publicar_novo_aviso) # Chamada aqui
            self.btn_add.pack(pady=5, padx=10)

            self.btn_del = CTkButton(self.frame_adm, text="- Apagar Aviso", 
                                     fg_color="#e74c3c", hover_color="#c0392b")
            self.btn_del.pack(pady=5, padx=10)

        elif self.tipo_usuario == "visitante":
            # Aviso para visitantes
            self.label_vis = CTkLabel(self.sidebar, text="Modo Visualização", text_color="gray")
            self.label_vis.pack(side="bottom", pady=20)
            
    def publicar_novo_aviso(self):
        mensagem = self.entry_novo_aviso.get()
        
        if mensagem.strip() != "":
            try:
                # Sua lógica de banco que já está pronta
                postagem(msg=mensagem)
                
                self.entry_novo_aviso.delete(0, 'end')
                sucesso = print("Postado com sucesso!")
                
                # self.carregar_avisos_no_mural() # Criaremos essa para ler o banco e exibir
            except Exception as e:
                print(f"Erro ao postar: {e}")
        else:
            print("O aviso não pode estar vazio!")
        if sucesso:
            self.carregar_avisos_no_mural()
            
    def carregar_avisos_no_mural(self):
    # 1. Limpa o mural antes de carregar (para não duplicar ao atualizar)
        for widget in self.mural_scrolling.winfo_children():
            widget.destroy()

        # 2. Busca os dados no banco (ordenando pelo ID mais recente primeiro)
        query = "SELECT mensagem, data FROM infos WHERE estado = 1 ORDER BY id DESC"
        
        with gerenciar_db() as cursor:
            cursor.execute(query)
            avisos = cursor.fetchall()

        # 3. Cria os "Cards" de aviso na tela
        for msg, data in avisos:
            # Criamos um frame para cada aviso (o "container")
            card = CTkFrame(self.mural_scrolling, fg_color="#333333", corner_radius=10)
            card.pack(fill="x", padx=10, pady=5)

            # O texto do aviso (Não editável)
            # O wraplength faz o texto quebrar linha automaticamente
            label_msg = CTkLabel(card, text=msg, 
                                wraplength=500, 
                                justify="left",
                                font=("Arial", 13))
            label_msg.pack(padx=15, pady=(10, 5), anchor="w")

            # A data da postagem (embaixo, menorzinha)
            label_data = CTkLabel(card, text=f"Postado em: {data}", 
                                font=("Arial", 10), 
                                text_color="gray")
            label_data.pack(padx=15, pady=(0, 10), anchor="e")

    def abrir_menu(self):
        # Aqui você chamará a classe do Menu passando o tipo_usuario
        print(f"Abrindo menu para nível: {self.tipo_usuario}")
        
    

if __name__ == "__main__":
    # Teste mudando para 'administrador', 'comum' ou 'visitante'
    app = MuralInformativo(tipo_usuario="administrador")
    app.mainloop()