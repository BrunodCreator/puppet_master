import customtkinter as ctk
import tkinter as tk
import os
import subprocess
from PIL import Image, ImageTk
import win32api, win32gui, win32ui, win32con
from functools import partial
from funcoes.executar_robo import executar_robo
from funcoes.finalizar_robo import finalizar_robo
from interface.calendario.tela_agendamento import abrir_janela_agendamento

def menu_principal():
    # Criar janela principal
    janela = ctk.CTk()
    janela.geometry('1000x600')
    # set_appearance_mode("dark")
    janela.title("ＰＵＰＰＥＴ   ＭＡＳＴＥＲ")
    janela.iconbitmap("puppet_master.ico")

    # Criar um frame rolável para exibir os executáveis
    frame_lista = ctk.CTkScrollableFrame(janela, fg_color="gray20", width=580, height=300)
    frame_lista.pack(pady=1, padx=0, fill="both", expand=True)

    checkboxes = {}
    executaveis = []
    # Criar um dicionário global para armazenar os processos

    processos_ativos = {}

    # Função intermediária para executar o robô e atualizar processos_ativos
    def iniciar_robo():
        global processos_ativos  # Permite modificar a variável global
        novos_processos = executar_robo(robo_selecionado, pasta_robos)  # Obtém o dicionário retornado
        processos_ativos.update(novos_processos)  # Atualiza os processos ativos


    pasta_base = os.path.dirname(os.path.abspath(__file__))
    pasta_robos = os.path.abspath(os.path.join(pasta_base, '..', 'robos'))
    
    print(f"Pasta de robôs: {pasta_robos}")  # Verificação do caminho correto

    # Criar a pasta se ela não existir
    if not os.path.exists(pasta_robos):
        os.makedirs(pasta_robos)

    robo_selecionado = tk.StringVar(value='')  # Nome do robô selecionado
    icones_carregados = {}  # Dicionário para armazenar os ícones carregados e evitar coleta de lixo

    # Função para extrair o ícone do executável
    def extrair_icone(caminho_exe):
        try:
            # Obter dimensões padrão do ícone
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

            # Extrair os handles do ícone (grande e pequeno)
            large_icons, small_icons = win32gui.ExtractIconEx(caminho_exe, 0)
            if small_icons:
                win32gui.DestroyIcon(small_icons[0])  # Libera o ícone pequeno

            hicon = large_icons[0] if large_icons else None
            if hicon is None:
                return None  # Se não houver ícone, retorna None

            # Criar um DC compatível e um bitmap compatível
            hdc_screen = win32gui.GetDC(0)
            hdc_mem = win32ui.CreateDCFromHandle(hdc_screen)
            hdc_compat = hdc_mem.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(hdc_mem, ico_x, ico_y)

            # Desenhar o ícone no bitmap
            hdc_compat.SelectObject(bmp)
            hdc_compat.DrawIcon((0, 0), hicon)

            # Obter os bits do bitmap e converter para imagem PIL
            bmp_bits = bmp.GetBitmapBits(True)
            icon_image = Image.frombuffer('RGBA', (ico_x, ico_y), bmp_bits, 'raw', 'BGRA', 0, 1)

            # Liberar recursos
            win32gui.DestroyIcon(hicon)
            hdc_compat.DeleteDC()
            win32gui.ReleaseDC(0, hdc_screen)
            win32gui.DeleteObject(bmp.GetHandle())

            return icon_image.resize((64, 64))  # Redimensiona o ícone para um tamanho adequado
        except Exception as e:
            print(f"Erro ao extrair ícone: {e}")
            return None  # Retorna None caso falhe

    # Função para buscar arquivos .exe na pasta selecionada
    def buscar_na_pasta():
        global executaveis
        executaveis = [f for f in os.listdir(pasta_robos) if f.endswith('.exe')]
        
        
        print(f'Robos  detectados: {executaveis}')
        # Atualizar a lista exibida
        atualizar_lista()

    # Função para atualizar a interface com os arquivos encontrados
    def atualizar_lista():
        global executaveis
        for widget in frame_lista.winfo_children():
            widget.destroy()  # Limpa a lista antes de atualizar

        global icones_carregados
        icones_carregados = {}  # Resetar dicionário de ícones para evitar coleta de lixo
        global checkboxes
        checkboxes = {}
        
        for exe in executaveis:
            caminho_exe = os.path.join(pasta_robos, exe)
            
            # Criar um frame para cada robô
            frame_robo = ctk.CTkFrame(frame_lista)
            frame_robo.pack(fill='x', pady=6, padx=3)

            # Tentar extrair o ícone do executável
            icone_exe = extrair_icone(caminho_exe)
            if icone_exe:
                icones_carregados[exe] = ImageTk.PhotoImage(icone_exe)  # Armazena a imagem para evitar coleta de lixo
                icone_img = icones_carregados[exe]
            else:
                icone_img = None  # Caso o ícone não seja encontrado, usar um padrão

            # Exibir o ícone real ou um ícone genérico
            if icone_img:
                icone_label = tk.Label(frame_robo, image=icone_img, width=64, height=64) # Define o tamanho da label
                icone_label.image = icone_img  # Mantém referência
                icone_label.pack(side="left", padx=6, pady=3)
            else:
                icone_label = ctk.CTkLabel(frame_robo, text="🤖", font=("Arial", 20))
                icone_label.pack(side="left", padx=6, pady=3)

            # Nome do arquivo .exe
            label_nome = ctk.CTkLabel(frame_robo, text=exe, font=("Arial", 14))
            label_nome.pack(side="left", padx=10, pady=5)

            # Criar um checkbox para selecionar o robô
            checkboxes[exe] = ctk.BooleanVar(value=False) #Criar variável para armazenar estado
            checkbox = ctk.CTkCheckBox(
                frame_robo, text='', variable=checkboxes[exe],
                command=partial(selecionar_robo, exe) #chama função ao clicar
            )

            checkbox.pack(side="right", padx=0, pady=0)


    def selecionar_robo(nome):
        """Altera a seleção do robô baseado no estado do checkbox. Permite apenas um robô selecionado por vez."""
        global checkboxes  # Garante que estamos alterando a variável global corretamente

        # Primeiro, desmarcar todos os checkboxes
        for robo, var in checkboxes.items():
            var.set(False)

        # Marcar apenas o checkbox do robô selecionado
        checkboxes[nome].set(True)

        # Atualizar a variável do robô selecionado
        robo_selecionado.set(nome)
        print(f"Robô selecionado: {nome}")  # Debugging para verificar a seleção

        # Habilitar os botões após a seleção
        btn_executar.configure(state="normal") 
        btn_finalizar.configure(state="normal")
        btn_agendar_execucao.configure(state="normal")
        btn_relatorio_execucao.configure(state="normal")

        

    # Criar frame inferior para os botões
    frame_botoes = ctk.CTkFrame(janela, fg_color="gray20")
    frame_botoes.pack(fill="x", pady=0, padx=0)  # Mais espaçamento nas bordas

    # Configurar a grade com 4 colunas
    frame_botoes.columnconfigure((0, 1, 2, 3), weight=1, uniform="botoes")  # Distribui o espaço igualmente

    # Criar os botões e posicioná-los na grade
    btn_relatorio_execucao = ctk.CTkButton(frame_botoes, text="Consultar Execução", state="disabled")
    btn_relatorio_execucao.grid(row=0, column=0, padx=10, pady=5, sticky="ew")  # "ew" expande horizontalmente

    btn_agendar_execucao = ctk.CTkButton(frame_botoes, text="Agendar Execução",command=lambda: abrir_janela_agendamento(robo_selecionado.get()) , state="disabled")
    btn_agendar_execucao.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    btn_executar = ctk.CTkButton(frame_botoes, text="Executar",command=lambda: iniciar_robo(), state="disabled")
    btn_executar.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

    btn_finalizar = ctk.CTkButton(frame_botoes, text="Finalizar",command=lambda: finalizar_robo(robo_selecionado, processos_ativos),  state="disabled")
    btn_finalizar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")




    # Buscar os robôs automaticamente ao iniciar o programa
    buscar_na_pasta()

    # Rodar a aplicação
    janela.mainloop()
    
    
    
