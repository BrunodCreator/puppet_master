import customtkinter as ctk
import tkinter as tk
import os
import subprocess
from PIL import Image, ImageTk
import win32api, win32gui, win32ui, win32con
from functools import partial
from funcoes.executar_robo import executar_robo
from funcoes.finalizar_robo import finalizar_robo
from interface.calendario.tela_agendamento import TelaAgendamento
from interface.tela_base import TelaBase

class MenuPrincipal(TelaBase):
    def __init__(self, janela_pai=None):
        # Inicializar a classe base
        super().__init__()
        
        if janela_pai:
            # Se uma janela pai for fornecida, destrua a janela criada pela classe base
            # e use a janela pai
            self.janela.destroy()
            self.janela = janela_pai
        
        # Alterar o título para indicar que estamos no menu principal
        self.alterar_titulo("ＭＥＮＵ   ＰＲＩＮＣＩＰＡＬ")

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

        # Inicializar os ícones carregados e botões
        self.icones_carregados = {}

        # Criar botões e estrutura de interface
        self.criar_botoes()
        self.buscar_na_pasta()

    def criar_botoes(self):
        """Cria os botões no rodapé da interface."""
        frame_botoes = ctk.CTkFrame(self.janela, fg_color="gray20")
        frame_botoes.pack(fill="x", pady=0, padx=0)

        frame_botoes.columnconfigure((0, 1, 2, 3), weight=1, uniform='botoes')

        self.btn_relatorio_execucao = ctk.CTkButton(frame_botoes, text='Consultar Execução', state='disabled', height=40)
        self.btn_relatorio_execucao.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

        self.btn_agendar_execucao = ctk.CTkButton(frame_botoes, text='Agendar Execução',
                                                 command=self.abrir_tela_agendamento,
                                                 state='disabled', height=40)
        self.btn_agendar_execucao.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.btn_executar = ctk.CTkButton(frame_botoes, text='Executar',
                                          command=self.iniciar_robo, state='disabled', height=40)
        self.btn_executar.grid(row=0, column=3, padx=10, pady=5, sticky='ew')

        self.btn_finalizar = ctk.CTkButton(frame_botoes, text='Finalizar',
                                           command=lambda: finalizar_robo(self.robo_selecionado, self.processos_ativos),
                                           state='disabled', height=40)
        self.btn_finalizar.grid(row=0, column=2, padx=10, pady=5, sticky='ew')

    def abrir_tela_agendamento(self):
        """Abre a tela de agendamento na mesma janela"""
        # Limpar a janela atual
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Criar e exibir a tela de agendamento na mesma janela
        tela_agendamento = TelaAgendamento(self.janela, self.robo_selecionado.get(), self)
        
    def iniciar_robo(self):
        """Inicia o robô selecionado."""
        novos_processos = executar_robo(self.robo_selecionado.get(), self.pasta_robos)
        self.processos_ativos.update(novos_processos)

    def buscar_na_pasta(self):
        """Busca os executáveis na pasta dos robôs e atualiza a lista"""
        self.executaveis = [f for f in os.listdir(self.pasta_robos) if f.endswith('.exe')]
        self.atualizar_lista()

    def atualizar_lista(self):
        """Atualiza a lista de executáveis na pasta dos robôs e atualiza a lista."""
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        self.icones_carregados = {}
        self.checkboxes = {}

        for exe in self.executaveis:
            caminho_exe = os.path.join(self.pasta_robos, exe)

            # Criar um frame para o robô
            frame_robo = ctk.CTkFrame(self.frame_lista)
            frame_robo.pack(fill='x', pady=6, padx=3)

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
                icone_label.pack(side='left', padx=6, pady=3)

            # Criar o nome do arquivo .exe como uma label
            label_nome = ctk.CTkLabel(frame_robo, text=exe, font=('Arial', 14))
            label_nome.pack(side='left', padx=10, pady=5)

            # Criar um checkbox para selecionar o robô
            self.checkboxes[exe] = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(frame_robo, text='', variable=self.checkboxes[exe],
                                       command=partial(self.selecionar_robo, exe))
            checkbox.pack(side="right", padx=0, pady=0)

    def selecionar_robo(self, nome):
        """Altera a seleção do robô baseado no estado do checkbox."""
        for robo, var in self.checkboxes.items():
            var.set(False)
        self.checkboxes[nome].set(True)
        self.robo_selecionado.set(nome)

        self.btn_executar.configure(state='normal')
        self.btn_finalizar.configure(state='normal')
        self.btn_agendar_execucao.configure(state='normal')
        self.btn_relatorio_execucao.configure(state='normal')

    def extrair_icone(self, caminho_exe):
        """Extrai o ícone do executável."""
        try:
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
            large_icons, small_icons = win32gui.ExtractIconEx(caminho_exe, 0)
            if small_icons:
                win32gui.DestroyIcon(small_icons[0])

            hicon = large_icons[0] if large_icons else None
            if not hicon:
                return None

            hdc_screen = win32gui.GetDC(0)
            hdc_mem = win32ui.CreateDCFromHandle(hdc_screen)
            hdc_compat = hdc_mem.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(hdc_mem, ico_x, ico_y)
            hdc_compat.SelectObject(bmp)
            hdc_compat.DrawIcon((0, 0), hicon)

            bmp_bits = bmp.GetBitmapBits(True)
            icon_image = Image.frombuffer('RGBA', (ico_x, ico_y), bmp_bits, 'raw', 'BGRA', 0, 1)

            win32gui.DestroyIcon(hicon)
            hdc_compat.DeleteDC()
            win32gui.ReleaseDC(0, hdc_screen)
            win32gui.DeleteObject(bmp.GetHandle())

            return icon_image.resize((64, 64))
        except Exception as e:
            print(f"Erro ao extrair ícone: {e}")
            return None

    def run(self):
        """Inicia a interface gráfica."""
        self.exibir()
        
    def voltar_ao_menu(self):
        """Métodos para voltar ao menu principal"""
        # Limpar a janela atual
        for widget in self.janela.winfo_children():
            widget.destroy()
            
        # Reinicializar o menu principal
        self.__init__(self.janela)
