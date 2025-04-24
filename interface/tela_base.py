import customtkinter as ctk
import os

class TelaBase:
    def __init__(self):
        self.janela = ctk.CTk()
        #Caminho do diretório onde o script atual está localizado
        self.pasta_interface = os.path.dirname(os.path.abspath(__file__))
        #Construir o caminho absoluto para o ícone
        icone_path = os.path.join(self.pasta_interface, 'puppet_master.ico')
        self.janela.geometry('1000x600')
        self.janela.title("ＰＵＰＰＥＴ   ＭＡＳＴＥＲ")
        self.janela.iconbitmap(icone_path)

    def alterar_titulo(self, nome_da_janela):
        """Métodos para alterar o título da janela dinamincamente"""
        self.janela.title(f'ＰＵＰＰＥＴ   ＭＡＳＴＥＲ   -->   {nome_da_janela}')



    def exibir(self):
        """Métodos para exibir a janela"""
        self.janela.mainloop()


if __name__ == '__main__':
    app = TelaBase()
    app.exibir()

