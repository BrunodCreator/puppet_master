import os
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import win32api
import win32gui
import win32con
import win32ui
from functools import partial
from funcoes.executar_robo import executar_robo
from funcoes.finalizar_robo import finalizar_robo
from interface.calendario.tela_agendamento import abrir_janela_agendamento

class MenuPrincipal:
    def __init__(self):
        # Criar janela principal
        self.janela = ctk.CTk()
        self.janela.geometry('1000x600')
        self.janela.title("\uff30\uff35\uff30\uff30\uff25\uff34   \uff2d\uff21\uff33\uff34\uff25\uff32")
        self.janela.iconbitmap("puppet_master.ico")

        # Diretórios e variáveis
        self.pasta_base = os.path.dirname(os.path.abspath(__file__))
        self.pasta_robos = os.path.abspath(os.path.join(self.pasta_base, '..','..', 'robos'))
        self.robo_selecionado = tk.StringVar(value='')

        if not os.path.exists(self.pasta_robos):
            print('A pasta de robôs não foi encontrada')

        # Criar um frame rolável para exibir os executáveis
        self.frame_lista = ctk.CTkScrollableFrame(self.janela, fg_color="gray20", width=580, height=300)
        self.frame_lista.pack(pady=1, padx=0, fill="both", expand=True)

        self.checkboxes = {}
        self.executaveis = []
        self.processos_ativos = {}
        self.icones_carregados = {}  # Dicionário para armazenar as imagens carregadas

        # Criar botões
        self.criar_botoes()

        # Atualizar a lista de executáveis
        self.atualizar_lista()

    def criar_botoes(self):
        """Cria os botões no rodapé da interface."""
        frame_botoes = ctk.CTkFrame(self.janela, fg_color="gray20")
        frame_botoes.pack(fill="x", pady=0, padx=0)

        frame_botoes.columnconfigure((0, 1, 2, 3), weight=1, uniform='botoes')

        self.btn_relatorio_execucao = ctk.CTkButton(frame_botoes, text='Consultar Execução', state='disabled')
        self.btn_relatorio_execucao.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        self.btn_agendar_execucao = ctk.CTkButton(frame_botoes, text='Agendar Execução',
                                                 command=lambda: abrir_janela_agendamento(self.robo_selecionado.get()),
                                                 state='disabled')
        self.btn_agendar_execucao.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.btn_executar = ctk.CTkButton(frame_botoes, text='Executar',
                                          command=self.iniciar_robo, state='disabled')
        self.btn_executar.grid(row=0, column=3, padx=10, pady=5, sticky='ew')

        self.btn_finalizar = ctk.CTkButton(frame_botoes, text='Finalizar',
                                           command=lambda: finalizar_robo(self.robo_selecionado, self.processos_ativos),
                                           state='disabled')
        self.btn_finalizar.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

    def iniciar_robo(self):
        """Inicia o robô selecionado."""
        novos_processos = executar_robo(self.robo_selecionado.get(), self.pasta_robos)
        if novos_processos:
            self.processos_ativos[self.robo_selecionado.get()] = novos_processos
            print(f"Processos ativos: {self.processos_ativos}")

    def atualizar_lista(self):
        """Atualiza a lista de executáveis disponíveis."""
        # Limpar a lista atual
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Limpar o dicionário de checkboxes
        self.checkboxes.clear()

        # Limpar a lista de executáveis
        self.executaveis.clear()

        # Limpar o dicionário de ícones carregados
        self.icones_carregados.clear()

        # Verificar se a pasta de robôs existe
        if not os.path.exists(self.pasta_robos):
            print('A pasta de robôs não foi encontrada')
            return

        # Listar todos os arquivos .exe na pasta de robôs
        for exe in os.listdir(self.pasta_robos):
            if exe.endswith('.exe'):
                self.executaveis.append(exe)

        # Criar um frame para cada executável
        for exe in self.executaveis:
            frame_robo = ctk.CTkFrame(self.frame_lista, fg_color="gray15", corner_radius=10)
            frame_robo.pack(fill="x", pady=5, padx=10)

            # Caminho completo para o executável
            caminho_exe = os.path.join(self.pasta_robos, exe)

            # Extrair o ícone do executável
            icone_exe = self.extrair_icone(caminho_exe)
            
            # Adicionar o ícone ou texto (se o ícone não for encontrado)
            if icone_exe:
                # Converter a imagem PIL para um formato que o Tkinter possa usar
                tk_image = ImageTk.PhotoImage(icone_exe)
                # Armazenar a imagem no dicionário para evitar coleta de lixo
                self.icones_carregados[exe] = tk_image
                
                icone_label = tk.Label(frame_robo, image=self.icones_carregados[exe], width=64, height=64)
                icone_label.pack(side="left", padx=6, pady=3)
            else:
                icone_label = ctk.CTkLabel(frame_robo, text='sem ícone', font=("Arial", 20))
                icone_label.pack(side="left", padx=6, pady=3)

            # Adicionar o nome do executável
            nome_label = ctk.CTkLabel(frame_robo, text=exe, font=("Arial", 14))
            nome_label.pack(side="left", padx=10, pady=3)

            # Adicionar o checkbox
            var = tk.BooleanVar(value=False)
            self.checkboxes[exe] = var

            # Criar um frame para o checkbox (para posicioná-lo à direita)
            frame_checkbox = ctk.CTkFrame(frame_robo, fg_color="transparent")
            frame_checkbox.pack(side="right", padx=10, pady=3)

            checkbox = ctk.CTkCheckBox(frame_checkbox, text="", variable=var, onvalue=True, offvalue=False,
                                      command=lambda nome=exe: self.selecionar_robo(nome))
            checkbox.pack(side="right")

            # Tornar o frame clicável
            frame_robo.bind("<Button-1>", lambda event, nome=exe: self.selecionar_robo(nome))
            nome_label.bind("<Button-1>", lambda event, nome=exe: self.selecionar_robo(nome))
            icone_label.bind("<Button-1>", lambda event, nome=exe: self.selecionar_robo(nome))

    def selecionar_robo(self, nome):
        """Seleciona um robô da lista."""
        # Desmarcar todos os checkboxes
        for exe, var in self.checkboxes.items():
            if exe != nome:
                var.set(False)

        # Marcar o checkbox do robô selecionado
        self.checkboxes[nome].set(True)
        self.robo_selecionado.set(nome)

        self.btn_executar.configure(state='normal')
        self.btn_finalizar.configure(state='normal')
        self.btn_agendar_execucao.configure(state='normal')
        self.btn_relatorio_execucao.configure(state='normal')

    def extrair_icone(self, caminho_exe):
        """Extrai o ícone do executável."""
        try:
            # Obter o ícone grande do executável
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

            large, small = win32gui.ExtractIconEx(caminho_exe, 0)
            if large:
                win32gui.DestroyIcon(small[0])  # Liberar o ícone pequeno

                # Criar um DC e um bitmap para o ícone
                hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
                hdc = hdc.CreateCompatibleDC()

                # Desenhar o ícone no bitmap
                hdc.SelectObject(hbmp)
                hdc.DrawIcon((0, 0), large[0])
                win32gui.DestroyIcon(large[0])  # Liberar o ícone grande

                # Converter o bitmap para uma imagem PIL
                bmpinfo = hbmp.GetInfo()
                bmpstr = hbmp.GetBitmapBits(True)
                img = Image.frombuffer(
                    'RGBA',
                    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                    bmpstr, 'raw', 'BGRA', 0, 1
                )

                # Redimensionar a imagem para 64x64
                img = img.resize((64, 64), Image.LANCZOS)

                return img
            return None
        except Exception as e:
            print(f"Erro ao extrair ícone: {e}")
            return None

    def run(self):
        """Inicia a interface gráfica."""
        self.janela.mainloop()
