import customtkinter as ctk


class TelaBase:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.geometry('1000x600')
        self.janela.title("ＰＵＰＰＥＴ   ＭＡＳＴＥＲ")
        #self.janela.title(f'PUPPET MASTER')
        #self.janela.title(f'PUPPET MASTER - {nome_janela}')
        self.janela.iconbitmap('puppet_master.ico')


    def exibir(self):
        """Métodos para exibir a janela"""
        self.janela.mainloop()


if __name__ == '__main__':
    app = TelaBase()
    app.exibir()

