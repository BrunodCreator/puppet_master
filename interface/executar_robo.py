import customtkinter as ctk
import tkinter as tk
import os
import subprocess
from PIL import Image, ImageTk
import win32api, win32gui, win32ui, win32con


def executar_robo(robo_selecionado, pasta_robos):
    processos_ativos = {}
    if robo_selecionado.get():
        caminho_exe = os.path.join(pasta_robos, robo_selecionado.get())
        try:
            processo = subprocess.Popen(caminho_exe, shell=True)  # Executa o arquivo
            processos_ativos[robo_selecionado.get()] = processo # Armazena o processo
            print(f"Robô {robo_selecionado.get()} iniciado! ")
            return processos_ativos
        except Exception as e:
             print(f"Erro ao executar {caminho_exe}: {e}")
    return {}  # Retorna um dicionário vazio caso falhe