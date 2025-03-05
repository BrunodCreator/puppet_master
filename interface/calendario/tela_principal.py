import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

# Lista para armazenar agendamentos
agendamentos = []

def abrir_janela_agendamento(robo_nome):
    """Abre uma janela para selecionar a data/hora de execução do robô"""
    if not robo_nome:
        print('Nenhum robô selecionado para agendar!')
        return  # Evita abrir a janela se nenhum robô estiver selecionado
    
    janela_agendamento = ctk.CTkToplevel()
    janela_agendamento.title("Agendar Execução")
    janela_agendamento.geometry("600x400")

    # Configurando a grade para alinhar corretamente os elementos
    janela_agendamento.columnconfigure(0, weight=1)
    janela_agendamento.rowconfigure(3, weight=1)  # Permite empurrar o botão para baixo

    # Criar rótulo para o título
    label_titulo = ctk.CTkLabel(janela_agendamento, text=f"Agendando execução para: {robo_nome}")
    label_titulo.grid(row=0, column=0, pady=10, sticky="n")

    # Criar o calendário para selecionar a data
    cal = Calendar(janela_agendamento, selectmode="day", year=2024, month=2, day=28)
    cal.grid(row=1, column=0, pady=10, sticky="n")

    # Campo para selecionar o horário
    entry_hora = ctk.CTkEntry(janela_agendamento, placeholder_text="Hora (HH:MM)")
    entry_hora.grid(row=2, column=0, pady=5, sticky="n")

    def confirmar_agendamento():
        """Confirma o agendamento e armazena a data/hora"""
        data_selecionada = cal.get_date()
        hora_selecionada = entry_hora.get()

        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")

            # Adicionar à lista de agendamentos
            agendamentos.append((robo_nome, horario_agendado))
            print(f"Robô {robo_nome} agendado para {horario_agendado}")

            janela_agendamento.destroy()  # Fechar janela
        except ValueError:
            print("Formato de horário inválido. Use HH:MM")

    # Criando um frame para o botão na parte inferior
    frame_botoes = ctk.CTkFrame(janela_agendamento)
    frame_botoes.grid(row=3, column=0, sticky="s", pady=10)

    # Criando o botão dentro do frame e posicionando corretamente
    btn_agendar = ctk.CTkButton(frame_botoes, text="Agendar", command=confirmar_agendamento)
    btn_agendar.grid(row=0, column=0, pady=0)
