import tkinter as tk
from tkinter import *
from customtkinter import CTk, CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu, CTkScrollableFrame, CTkTextbox, CTkToplevel
from tkinter import messagebox

from banco.banco_usuarios import *
from banco.banco_infos import *
from Interface.entidades import usuarios

# Cria classe do Mural Informativo
# A Interfce que exibe os avisos para os usuários
# Tem diferentes níveis de acesso a funcionalidades.
class MuralInformativo(CTk):
    def __init__(self, tipo_usuario="comum", id_usuario=None):
        super().__init__()
        self.tipo_usuario = tipo_usuario
        self.id_usuario_logado = id_usuario
        self.title(f"Ruralinfo - Mural ({self.tipo_usuario.capitalize()})")
        self.geometry("800x600")

        # Layout principal
        self.sidebar = CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.conteudo = CTkFrame(self, fg_color="transparent")
        self.conteudo.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Elementos fixos (todos veem)
        self.label_titulo = CTkLabel(self.conteudo, text="Mural de Avisos", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=10)

        self.mural_scrolling = CTkScrollableFrame(self.conteudo, label_text="Avisos Recentes")
        self.mural_scrolling.pack(fill="both", expand=True, pady=10)

        # Botão de menu (todos veem)
        self.btn_menu = CTkButton(self.sidebar, text="Acessar Menu", command=self.abrir_menu)
        self.btn_menu.pack(pady=20, padx=10)
        
        self.btn_perfil = CTkButton(self.sidebar, text="👤 Meu Perfil", 
                            fg_color="transparent", border_width=1,
                            command=self.abrir_perfil)
        self.btn_perfil.pack(pady=10, padx=10)

        # Lógica de permissões
        self.montar_ferramentas_especificas()
        self.carregar_avisos_no_mural()

    # utilidades específicas para cada tipo de usuário
    def montar_ferramentas_especificas(self):
        """Injeta botões e campos baseados no nível de acesso"""
        
        if self.tipo_usuario == "administrador":
            self.frame_adm = CTkFrame(self.sidebar, fg_color="transparent")
            self.frame_adm.pack(pady=10, fill="x")

            self.entry_novo_aviso = CTkEntry(self.frame_adm, placeholder_text="Escreva o aviso aqui...")
            self.entry_novo_aviso.pack(pady=5, padx=10)

            # botão aponta para a função publicar_novo_aviso
            self.btn_add = CTkButton(self.frame_adm, text="+ Adicionar Aviso", 
                                     fg_color="green", hover_color="#1e7b4d",
                                     command=self.publicar_novo_aviso)
            self.btn_add.pack(pady=5, padx=10)

        elif self.tipo_usuario == "visitante":
            # Aviso para visitantes
            self.label_vis = CTkLabel(self.sidebar, text="Modo Visualização", text_color="gray")
            self.label_vis.pack(side="bottom", pady=20)
    
    # cria a função para publicar um novo aviso
    def publicar_novo_aviso(self):
        mensagem = self.entry_novo_aviso.get()
        
        if mensagem.strip() != "":
            try:
                # Sua lógica de banco que já está pronta
                postagem(msg=mensagem)
                
                self.entry_novo_aviso.delete(0, 'end')
                print("Postado com sucesso!")
                
                # self.carregar_avisos_no_mural() # Criaremos essa para ler o banco e exibir
            except Exception as e:
                print(f"Erro ao postar: {e}")
        else:
            print("O aviso não pode estar vazio!")

        self.carregar_avisos_no_mural()
            
    def carregar_avisos_no_mural(self):
    # limpa o mural
        for widget in self.mural_scrolling.winfo_children():
            widget.destroy()

        # busca os dados no banco
        query = "SELECT id, mensagem, data FROM infos WHERE estado = 1 ORDER BY id DESC"
        
        with gerenciar_db() as cursor:
            cursor.execute(query)
            avisos = cursor.fetchall()

        # cria os cards de aviso na tela
        for id_postagem, msg, data in avisos:
            # frame pra cada a viso
            card = CTkFrame(self.mural_scrolling, fg_color="#333333", corner_radius=10)
            card.pack(fill="x", padx=10, pady=5)

            label_msg = CTkLabel(card, text=msg, 
                                wraplength=500, 
                                justify="left",
                                font=("Arial", 13))
            label_msg.pack(padx=15, pady=(10, 5), anchor="w")

            # data da postagem (embaixo, menorzinha)
            label_data = CTkLabel(card, text=f"Postado em: {data}", 
                                font=("Arial", 10), 
                                text_color="gray")
            label_data.pack(padx=15, pady=(0, 10), anchor="e")
            
            if self.tipo_usuario.lower() == "administrador":
                btn_opcoes = CTkOptionMenu(card, 
                           values=["Editar", "Excluir"],
                           width=30,
                           height=20,
                           corner_radius=5,
                           fg_color="#333333",          
                           button_color="#333333",
                           button_hover_color="#444444",
                           dynamic_resizing=False,
                           command=lambda escolha, id_p=id_postagem, txt=msg: self.opcoes_aviso(escolha, id_p, txt))

                btn_opcoes.set("⋮") 
                btn_opcoes.pack(padx=10, pady=5, anchor="ne")
    
    #cria a função para editar ou excluir um aviso            
    def opcoes_aviso(self, escolha, id_p, texto_antigo):
        if escolha == "Editar":
            
            janela_editar = CTkToplevel(self)
            janela_editar.title("Editar Aviso")
            janela_editar.geometry("400x300")
            janela_editar.attributes("-topmost", True)
            
            campo_editar = CTkTextbox(janela_editar, width=350, height=200)
            campo_editar.pack(pady=20, padx=20)
            campo_editar.insert("0.0", texto_antigo)
            
            # função para confirmar a edição
            def confirmar():
                novo_texto = campo_editar.get("1.0", "end-1c")
                if novo_texto.strip() != "":
                    atualizar_posatagem(id_p, coluna='mensagem', estado_postagem=novo_texto)
                    janela_editar.destroy()
                    self.carregar_avisos_no_mural() # Atualiza o mural após edição
                else:
                    print("O aviso editado não pode estar vazio!")
        
            btn_salvar = CTkButton(janela_editar, text="Salvar Edição", command=confirmar)
            btn_salvar.pack(pady=10)
            
        elif escolha == "Excluir":
            apagar_postagem(id_p) 
            self.carregar_avisos_no_mural() # Atualiza o mural após exclusão

    #cria a função para abrir o perfil do usuário logado, onde ele pode ver seus dados e alterar a senha ou excluir a conta
    def abrir_perfil(self):
    # busca dados do banco
        dados = obter_dados_usuario(self.id_usuario_logado)
        
        if dados:
            nome_db, email_db, tipo_db = dados
        else:
            nome_db, email_db, tipo_db = "Erro", "Erro", "Erro"

        janela_perfil = CTkToplevel(self)
        janela_perfil.title("Meu Perfil - Ruralinfo")
        janela_perfil.geometry("400x520")
        janela_perfil.attributes("-topmost", True)

        CTkLabel(janela_perfil, text="Informações do Usuário", font=("Arial", 18, "bold")).pack(pady=20)

        # Exibição de Dados (Usando as variáveis vindas do banco)
        CTkLabel(janela_perfil, text=f"Nome: {nome_db}", anchor="w").pack(fill="x", padx=30)
        CTkLabel(janela_perfil, text=f"E-mail: {email_db}", anchor="w").pack(fill="x", padx=30)
        CTkLabel(janela_perfil, text=f"Tipo: {tipo_db.capitalize()}", anchor="w", text_color="gray").pack(fill="x", padx=30)

        # Troca de Senha
        CTkLabel(janela_perfil, text="\nAlterar Senha", font=("Arial", 14, "bold")).pack(pady=10)
        nova_senha = CTkEntry(janela_perfil, placeholder_text="Nova senha", show="*")
        nova_senha.pack(pady=5, padx=30, fill="x")
        confirmar_senha = CTkEntry(janela_perfil, placeholder_text="Confirme a nova senha", show="*")
        confirmar_senha.pack(pady=5, padx=30, fill="x")

        def salvar_senha():
            s1 = nova_senha.get()
            s2 = confirmar_senha.get()

            if s1 == s2 and len(s1) >= 4:
                atualizar_usuario(coluna="senha", valor=s1, id_usuario=self.id_usuario_logado)
                print("Senha alterada com sucesso!")
                janela_perfil.destroy()
            else:
                print("As senhas não coincidem ou são muito curtas!")

        btn_salvar = CTkButton(janela_perfil, text="Salvar Nova Senha", fg_color="green", command=salvar_senha)
        btn_salvar.pack(pady=20)

        # função para solicitar exclusão da conta
        def solicitar_exclusao_propria():
            if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir sua conta? Esta ação é permanente."):
                deletar_usuario(self.id_usuario_logado)
                janela_perfil.destroy()
                self.destroy() # Fecha o Mural
                
                #reinicia login
                janela_login = usuarios.TelaUsuario() 
                janela_login.mainloop()

        btn_excluir_conta = CTkButton(janela_perfil, text="Excluir Conta", 
                                    fg_color="red", hover_color="#8b0000",
                                    command=solicitar_exclusao_propria)
        btn_excluir_conta.pack(pady=20)
    
    # função para abrir o menu (ainda sem implementação)       
    def abrir_menu(self):
        # chamar a classe menu aqui, passando o tipo usuário
        print(f"Abrindo menu para nível: {self.tipo_usuario}")

if __name__ == "__main__":
    app = MuralInformativo(tipo_usuario="administrador")
    app.mainloop()