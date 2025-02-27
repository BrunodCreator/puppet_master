import customtkinter as ctk
import os
import tkinter as tk
from tkinter import filedialog
import subprocess
from menu_principal import frame_lista

executaveis = []
def buscar_na_pasta():
    pasta = filedialog.askdirectory(title="Buscar na pasta") 
    if not pasta:
        return #Se o usuário cancelar, não faz nada
    
    global executaveis
    executaveis = [f for f in os.listdir(pasta) if f.endswith('.exe')]
    
    #atualizar a lista exibida
    atualizar_lista(pasta)
    
#função para atualizar a interface com os arquivos encontrados
def atualizar_lista(caminho_pasta):
    for widget in frame_lista.winfo_children():
        widget.destroy() #limpa antes de atualizar
        
    for exe in executaveis:
        caminho_exe = os.path.join(caminho_pasta, exe)
        
        #Criar um frame para cada robô
        frame_robo = ctk.CTkFrame(frame_lista)
        frame_robo.pack(fill='x', pady=5, padx=5)
        
        #Icone generico do robô
        icone = ctk.CTkLabel(frame_robo, text="🤖", font=("Arial", 20))
        icone.pack(side="left", padx=10, pady=5)
        
        #Nome do arquivo .exe
        label_nome = ctk.CTkLabel(frame_robo, text=exe, font=("Arial", 14))
        label_nome.pack(side="left", padx=10, pady=5)
        
        #Botão para executar o arquivo 
        btn_executar = ctk.CTkButton(frame_robo, text="Executar", width=80, command=lambda p=caminho_exe: executar_exe(p))
        btn_executar.pack(side="right", padx=10, pady=5)
        
        
    def executar_exe(caminho_exe):
        try:
            subprocess.Popen(caminho_exe, shell=True) #Executa o arquivo
        except Exception as e:
            print(f'Erro ao executar {caminho_exe}: {e}')
            
            