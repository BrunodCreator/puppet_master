import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
import subprocess
from PIL import Image, ImageTk
import win32api, win32gui, win32ui, win32con

# Criar janela principal
janela = ctk.CTk()
janela.geometry('1000x600')
janela.title("ＰＵＰＰＥＴ_ＭＡＳＴＥＲ")
janela.iconbitmap("puppet_master.ico")

# Criar um frame rolável para exibir os executáveis
frame_lista = ctk.CTkScrollableFrame(janela, fg_color="gray20", width=580, height=300)
frame_lista.pack(pady=0, padx=0, fill="both", expand=True)

executaveis = []
pasta_selecionada = ''
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

        return icon_image.resize((32, 32))  # Redimensiona o ícone para um tamanho adequado
    except Exception as e:
        print(f"Erro ao extrair ícone: {e}")
        return None  # Retorna None caso falhe

# Função para buscar arquivos .exe na pasta selecionada
def buscar_na_pasta():
    global pasta_selecionada
    pasta = filedialog.askdirectory(title="Buscar na pasta") 
    if not pasta:
        return  # Se o usuário cancelar, não faz nada
    
    pasta_selecionada = pasta
    global executaveis
    executaveis = [f for f in os.listdir(pasta) if f.endswith('.exe')]
    
    # Atualizar a lista exibida
    atualizar_lista()

# Função para atualizar a interface com os arquivos encontrados
def atualizar_lista():
    for widget in frame_lista.winfo_children():
        widget.destroy()  # Limpa a lista antes de atualizar

    global icones_carregados
    icones_carregados = {}  # Resetar dicionário de ícones para evitar coleta de lixo
        
    for exe in executaveis:
        caminho_exe = os.path.join(pasta_selecionada, exe)
        
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
            icone_label = tk.Label(frame_robo, image=icone_img)
            icone_label.image = icone_img  # Mantém referência
            icone_label.pack(side="left", padx=6, pady=3)
        else:
            icone_label = ctk.CTkLabel(frame_robo, text="🤖", font=("Arial", 20))
            icone_label.pack(side="left", padx=6, pady=3)

        # Nome do arquivo .exe
        label_nome = ctk.CTkLabel(frame_robo, text=exe, font=("Arial", 14))
        label_nome.pack(side="left", padx=10, pady=5)

        # Botão para selecionar o robô
        btn_selecionar = ctk.CTkButton(
            frame_robo, text="Selecionar", width=80, 
            command=lambda nome=exe: selecionar_robo(nome)
        )
        btn_selecionar.pack(side="right", padx=10, pady=5)

# Função para definir o robô selecionado e ativar o botão "Executar"
def selecionar_robo(nome):
    robo_selecionado.set(nome)  # Atualiza a variável com o nome do robô
    btn_executar.configure(state="normal")  # Habilita o botão "Executar"

# Função para executar o robô selecionado
def executar_robo():
    if robo_selecionado.get():
        caminho_exe = os.path.join(pasta_selecionada, robo_selecionado.get())
        try:
            subprocess.Popen(caminho_exe, shell=True)  # Executa o arquivo
        except Exception as e:
            print(f"Erro ao executar {caminho_exe}: {e}")

# Criar frame inferior para os botões
frame_botoes = ctk.CTkFrame(janela, fg_color="gray30")
frame_botoes.pack(fill="x", pady=10, padx=10)

# Botão para selecionar a pasta
btn_carregar = ctk.CTkButton(frame_botoes, text="Selecionar Pasta", command=buscar_na_pasta)
btn_carregar.pack(side="left", padx=5, pady=5)

# Botão para executar o robô (inicialmente desativado)
btn_executar = ctk.CTkButton(frame_botoes, text="Executar", command=executar_robo, state="disabled")
btn_executar.pack(side="right", padx=5, pady=5)

# Rodar a aplicação
janela.mainloop()
