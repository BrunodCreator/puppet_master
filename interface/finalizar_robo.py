import customtkinter as ctk
import tkinter as tk
import os
import subprocess
from PIL import Image, ImageTk
import win32api, win32gui, win32ui, win32con
import psutil  # Biblioteca para gerenciar processos no Windows
import os
import win32gui
import win32con


def finalizar_robo(robo_selecionado, processos_ativos):
    """Finaliza completamente um robô e todos os processos relacionados"""
    nome_robo = robo_selecionado.get()
    
    if nome_robo in processos_ativos:
        try:
            # Obtém o objeto Popen do processo armazenado
            processo_principal = processos_ativos[nome_robo]
            pid_principal = processo_principal.pid  # Obtém o PID do processo principal
            
            # Converte para um objeto psutil.Process para obter o nome correto do processo
            processo_psutil = psutil.Process(pid_principal)
            nome_processo = processo_psutil.name()  # Nome real do executável do robô

            print(f"Tentando finalizar: {nome_processo} (PID: {pid_principal})")

            # **1️⃣ Finaliza TODOS os processos que tenham o mesmo nome do robô**
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                try:
                    if proc.info["name"].lower() == nome_processo.lower():
                        print(f"Matando processo: {proc.info['name']} (PID: {proc.pid})")
                        proc.kill()  # Mata o processo imediatamente
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            # **2️⃣ Se ainda existir, força o encerramento com `taskkill`**
            os.system(f"taskkill /F /IM \"{nome_processo}\" /T")

            # **3️⃣ Tenta encerrar pelo nome correto que aparece no Gerenciador de Tarefas**
            os.system(f"taskkill /F /IM \"Ministerio do desenv social.exe\" /T")

            # **4️⃣ Remove o robô do dicionário de processos ativos**
            processos_ativos.pop(nome_robo, None)
            print(f"Robô {nome_robo} finalizado com sucesso!")

        except Exception as e:
            print(f'Erro ao finalizar {nome_robo}: {e}')
    else:
        print("Nenhum robô em execução para finalizar.")
