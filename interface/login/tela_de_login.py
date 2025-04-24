from interface.tela_base import TelaBase
import customtkinter as ctk


class TelaLogin(TelaBase):
    def __init__(self):
        super().__init__()

        self.alterar_titulo('ＬＯＧＩＮ')

        # Criar um frame para o login (com fundo e um pouco de espaço)
        self.frame_login = ctk.CTkFrame(self.janela, fg_color="gray20", width=600, height=400)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")  # Centraliza o frame na tela

        # Criar o label e o campo de entrada para o usuário
        self.label_usuario = ctk.CTkLabel(self.frame_login, text="Usuário:")
        self.label_usuario.grid(row=0, column=0, padx=6, pady=3, sticky="w")  # Alinha à esquerda

        self.entry_usuario = ctk.CTkEntry(self.frame_login, width=300)
        self.entry_usuario.grid(row=1, column=0, padx=6, pady=3, sticky="ew")  # Preenche a largura da coluna

        # Criar o label e o campo de entrada para a senha
        self.label_senha = ctk.CTkLabel(self.frame_login, text="Senha:")
        self.label_senha.grid(row=2, column=0, padx=6, pady=3, sticky="w")

        self.entry_senha = ctk.CTkEntry(self.frame_login, show="*")
        self.entry_senha.grid(row=3, column=0, padx=6, pady=3, sticky="ew")  # Preenche a largura da coluna

        # Criar o botão de login
        self.botao_login = ctk.CTkButton(self.frame_login, text="Login", command=self.realizar_login)
        self.botao_login.grid(row=4, column=0, padx=10, pady=20, sticky="ew")

        # Adicionando letreiro no rodapé
        self.letreiro = ctk.CTkLabel(self.janela, text='Bem-vindo ao Puppet Master! Este projeto está sendo desenvolvido por Emerson Bruno, e agora tenho um letreiro de caminhão', font=("Arial", 14))
        self.letreiro.place(relx=0.8, rely=1, anchor='se')

        self.mover_texto()

    def realizar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        print(f"Usuário: {usuario}, Senha: {senha}")


    def mover_texto(self):
        # Pega a posição atual do letreiro
        current_x = self.letreiro.winfo_x()
        screen_width = self.janela.winfo_width()
        #atualiza a posição do letreiro para mover para a esquerda
        new_x = current_x - 0.001
        if new_x < -self.letreiro.winfo_width():
            new_x = screen_width

        self.letreiro.place(x=new_x, rely=1, anchor='se')

        self.janela.after(100, self.mover_texto)


if __name__ == '__main__':
    login = TelaLogin()
    login.exibir()
